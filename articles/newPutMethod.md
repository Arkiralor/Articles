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