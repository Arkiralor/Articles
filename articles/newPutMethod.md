# _PUT_ Request in a CRUD Application in _Django Rest Framework_

The __U__ in __CRUD__ stands for _Update_ and is one of the most basic operations one might need to deploy in a web-application backend.
But just because it happens to be one of the fundamental operations does not mean that implementing it has been made simple in various frameworks;
I do not know about the other popular backend frameworks but [Django](https://www.djangoproject.com/) via [Rest Framework](https://www.django-rest-framework.org/)
provides a truly bizzare implementation, let us take a look.

## Implementing the Model

Let us start by implementing a new model first.

### Creating the Model

To create the model, simply define a new model in the `models.py` file of your Django App like so.

![Sample Model](https://i.imgur.com/Aj2B3nd.png)

Do not worry about the `TemplateClass` parent we are inheriting from instead of `models.Model`, it is just an [`Abstract Model`](https://docs.djangoproject.com/en/4.1/topics/db/models/#abstract-base-classes) that I use to automatically add the fields `UUID id (Primary Key)`, `Datetime created (auto_now_add)` and `Datetime updated (auto_now)` so that I do not have to keep manually typing the code.

Now let us add a few more lines to make this a fully-fleshed-out model, mainly by adding some extra meta  options and an over-ridden `save()` function to auto-process some data upon model creation:

![Extra Model Configuration](https://i.imgur.com/bvuseN3.png)

### Creating the ModelSerializer

We will keep the serializer simple by implementing a simple [`serializers.ModelSerializer`](https://www.django-rest-framework.org/api-guide/serializers/#modelserializer) that comes pre-packaged in `Rest Framework` instead of creating a custom [`serializers.Serializer`](https://www.django-rest-framework.org/api-guide/serializers/#declaring-serializers) class.

![Model Serializer](https://i.imgur.com/KY3Fekm.png)

### Creating and Registering the ModelAdmin

Now that we have created the model and its associated serializer, we need to make the table visible in the __Admin Panel__ to make inspecting the data a bit easier. Let us do that in the `admin.py` page of our Django app.

![Model Admin](https://i.imgur.com/HRKBZam.png)

### Reminder

Do not forget to run:

1. `python manage.py makemigrations`
2. `pyhton manage.py migrate`

so that our model actually shows up in our Database as a table.

## Implementing the __CRUD__ API

Great, now that we have created the model and its associated configuration, we can start working on the API part of the rest API.

_To get to the point sooner, I will assume that you already know how to implement the basic __Create__, __List__, __Retrieve__ and __Destroy__ functionalities and instead will primarilly focus on the __Update__ functionality._

### Creating the PUT API

Let us now create a `PUT` method handler in the API (_you need not use the PUT method, but using the proper methods does make the intention of the endpoint clearer and makes the documentation easier to understand_).

![PUT API](https://i.imgur.com/gFtsriN.png)

As seen in the picture, we do the following steps in order

1. Retrive the object `id` (primary key) from the request.
2. Retrieve the object by querying the database via its primary key.
3. Insert the new data from the request into the object via an instance of its `ModelSerializer` that we defined earlier.
4. Check if the serializer object is valid
    - If it is not valid, return the error as an API response.
5. Save the serializer instance, thus commiting the changes to the model object and hence the database table row.

Simple, right? Now let us fire up [Postman](https://www.postman.com/) and make a simple PUT request to the server.

![Classic Put Request](https://i.imgur.com/QUW7zXS.png)

Here, now we know that it is working with a full set of data in the body, namely :

1. `name:str`
2. `char_field:str`
3. `decimal_field:float`
4. `integer_field:int`
5. `boolean_field:bool`

But what happens if we only want to change a single column/field in the row/object? Let us see for ourselves by trying to alter only the field `name` in the object.

![Invalid Classic PUT Request](https://i.imgur.com/ADr9Kiz.png)

Hmm, it seems we cannot use a serializer to update only a single field in the model object. This can be a problem; now of course, we can simple write

```python
    if "name" in request.data.keys():
        instance.name = request.data.get("name")
    if "char_field" in request.data.keys():
        instance.name = request.data.get("char_field")
    if "decimal_field" in request.data.keys():
        instance.name = request.data.get("decimal_field")
    if "integer_field" in request.data.keys():
        instance.name = request.data.get("integer_field")
    if "boolean_field" in request.data.keys():
        instance.name = request.data.get("boolean_field")
```

This, as all other working examples, is a valid implementation of the logic we want to implement. But do you not think that this code looks a bit cumbersome?
And I do not know about you, but I do not like the idea of giving up on Serializers for a single type of operation and all the benefits that come with it.

So how do we overcome this problem? See the code snippet above? Let us take it one step further with the following algorithm.

![Updated PUT Request](https://i.imgur.com/og9hiYR.png)

Now, what have we done differently this time around? Let us examine the steps.

1. Retrive the object `id` (primary key) from the request.
2. Retrieve the object by querying the database via its primary key.
3. Turn the object into a python `dictionary` by using its serializer.
4. Updated the values in the object dictionary with the values in the request body.
5. Inserted the new values into the object via its serializer from its own object disctionary with the updated values copied to it from the request body.
6. Check if the serializer object is valid
    - If it is not valid, return the error as an API response.
7. Save the serializer instance, thus commiting the changes to the model object and hence the database table row.

The key functionality of this code comes on stage in `line:190` as seen in the picture above.

```python
    for key in request.data.keys():
        obj_data[key] = request.data.get(key)
```

Now, let us fire up Postman again and see if this work. We will try to update the `name` field again.

![New PUT Request Response](https://i.imgur.com/uWqbKLg.png)

HEY! What do you know? It works. We used the dictionary update method and the dictionary keys method to overcome a major limitation of Django Rest Framework!

#### Expanded Functionality

But wait, this is not the end of it. This algorithm does double duty. Can you guess what would happen if we sent a blank request body? Think about it...the body is only used to update the values in the object dictionary, which is itself used to update the model instance. What would happen if the following were to happen?

```python
    keys = request.data.keys()
    => keys = None if request.data = dict()
```

So now, there are no keys in the request body therefore, the object dictionary is not updated, so according to our code, the response body would be nothing more than the object's original value, right?

Let us check.

![PUT Request with Blank Body](https://i.imgur.com/dofyLpt.png)

Hey! So this method handler also does double duty as a perfectly functional `RETRIEVE` API!

So with a tiny bit of Python knowhow, we not only overcame the basic update method's limitation(s) but expanded its functionality as well.

#### Adding API Constraints

"But Author, Author.", I hear you screaming out loud, "What if the user tries to alter a field that we do not want them to be able to alter?"
To which I reply with the following picture.

![Allowed Fields](https://i.imgur.com/1CPvxwl.png)

Simply add a list of allowed fields in the function/class and add the following line to the object dictionary update loop.

```python
    if key not in self.ALLOWED_FIELDS:
        return Response(
            {
                "error": f"Field '{key}' is not permitted to be altered"
            }
        )
```

This would make the complete loop look something like the following.

```python
    for key in request.data.keys():
        if key not in self.ALLOWED_FIELDS:
            return Response(
                {
                    "error": f"Field '{key}' is not permitted to be altered"
                }
            )
        obj_data[key] = request.data.get(key)
```

This assures that if the API requester tries to alter a field that they are not supposed to be able to alter, the API will return an error response.

## Conclusion

So in this article, we discussed how we can overcome a significant headache reagarding the model update method is Rest Framework and also how to expand its functionality to make it reusable in multiple use-cases. I apologize if this is common knowledge but I could not find many or any resources discussing this and this was a significant point of frustration for me, personally when I started with API.

Anyway, I hope this article may be of some use to you. The full source code for this article can be found on my [personal Github](https://github.com/Arkiralor/Articles/tree/master/src).

Until next time.
