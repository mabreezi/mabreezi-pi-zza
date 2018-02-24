# Interaction with Kibaati Ledger REST API
  
This app connects to the Kibaati Ledger REST API and is able to create new participants and items, submit transactions and make trades of assets.

## Usage

### Clone the repository
  
```
$ git clone https://github.com/kibaati/django-rest-api.git
```
  

### Run the development server
  
In the same folder that has the `manage.py` file, run the command below:

```
$ python manage.py runserver
```
  
This will start the application at `localhost:8000/hyper`.
  
### Navigate through the application
  
The application has 4 views, each presenting a form that performs a particular role:
* Add a new Person/Participant
* Add a new Item
* Send funds to another person
* Transfer an Item/Asset to another person

The 4 different applications are at the locations below respectively:
* add-person
* add-item
* submit-transaction
* make-trade

For example to get to the view to add a new person, navigate to `localhost:8000/hyper/add-person`.
