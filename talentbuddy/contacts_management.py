import pymongo

# Initialize connection and collections.
connection = pymongo.Connection('localhost:27017')
db = connection['contact_management']
contacts_collection = db['contacts']
mutations_collection = db['mutations']
# Create/ensure indexes
contacts_collection.ensure_index('email')
mutations_collection.ensure_index('contact_email')

def create_mutation(author, contact_email, field, value):
    doc = {
        'author': author,
        'contact_email': contact_email,
        'field': field,
        'value': value
    }
    mutations_collection.insert(doc)

def create_contact(author, contact_name, contact_email, contact_birthday):
    contact = {
        'email': contact_email,
        'name': contact_name,
        'birthday': contact_birthday
    }
    for field, value in contact.items():
        create_mutation(author, contact_email, field, value)
    contacts_collection.insert(contact)

def edit_contact(author, contact_email, field, value):
    query = {'email': contact_email}
    update = {field: value}
    contacts_collection.update(query, update)
    create_mutation(author, contact_email, field, value)

def field_history(contact_email, field):
    query = {
        'contact_email': contact_email,
        'field': field
    }
    mutations = mutations_collection.find(query)
    for mutation in mutations:
        print '%(author)s %(value)s' % mutation

def get_birthdays(month):
    # Birthday: '1988-03-20'
    regex = '....-%02d-..' % month
    query = {
        'birthday': { '$regex': regex }
    }
    cursor = contacts_collection.find(query)
    names = [d['name'] for d in cursor]
    names.sort()
    print '\n'.join(names)

create_contact('Auth1', 'John Sailor', 'john@google.com', '1960-03-20')
get_birthdays(3)
# create_contact('Auth1', 'John Sailor', 'john@google.com', '1960-03-20')

