import random
import string

class PasswordError(Exception):
    """Custom error to be used in UserMap when wrong password is given for a user."""
    def __init__(self, message):
        self.message = message
    def __repr__(self):
        return f"PasswordError: {repr(self.message)}"

class UserRecord:
    def __init__(self, username, password):
        self.username = username
        self.salt = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        self.password_hash = self.simple_hash(password)
    
    def simple_hash(self, password):
        """A simple hash function."""
        salted_password = password + self.salt
        return hash(salted_password)
    
    def __repr__(self):
        """Returns a string represention of a UserRecord."""
        return f"UserRecord: {self.username}"

class UserMap:
    def __init__(self):
        self._num_buckets = 8
        self._max_load_factor = .75
        self._len = 0
        self._buckets = [None for i in range(self._num_buckets)]
    
    def __len__(self):
        '''Returns the number of records stored in the database.'''
        return self._len


    def __getitem__(self, username):
        '''Returns the stored user recored for a given username, Raises KeyError if a record for the given username is not in the database.'''
        the_index = hash(username) % self._num_buckets
        bucket = self._buckets[the_index]
        if bucket is None or bucket.username != username:
            raise KeyError(f"No user record found for username: {username}")
        return bucket

    def __contains__(self, username):
        '''Returns True ( False ) if a given username is (is not) registered in the database.'''
        try:
            _ = self[username]
            return True
        except KeyError:
            return False

    def add_user(self, username, password):
        '''Adds a user record to the database using the given username and password'''
        '''This method should utilize linear probing to find the appropriate internal storage location for the user record.'''
        '''If the username is already registered in the database, this method should raise a RuntimeError .'''
        if username in self:
            raise RuntimeError(f"Username {username} already exists.")
        if self._len / self._num_buckets >= self._max_load_factor:
            self._double()
        the_index = hash(username) % self._num_buckets
        while self._buckets[the_index] is not None:
            the_index = (the_index + 1) % self._num_buckets
        self._buckets[the_index] = UserRecord(username, password)
        self._len += 1

    def update_password(self, username, current_password, new_password):
        '''Updates the user's password if and only if the supplied current_password is correct'''
        '''If username is not registered in the database, raises KeyError'''
        ''' current_password is incorrect, raises a PasswordError'''
        user_record = self[username]
        if user_record.simple_hash(current_password) != user_record.password_hash:
            raise PasswordError("Incorrect password.")
        user_record.salt = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        user_record.password_hash = user_record.simple_hash(new_password)
    
    def _double(self):
        '''Private method that is used to double the size of internal storage within the database
            when the number of records exceeds 75% (starter code already contains
            self._max_load_factor equal to 0.75) of the available storage locations
            (buckets). After increasing storage, all records in the database are rehashed.'''

        old_buckets = self._buckets
        self._num_buckets *= 2
        self._buckets = [None for i in range(self._num_buckets)]
        self._len = 0
        for user_record in old_buckets:
            if user_record is not None:
                #places the user record in the new bucket array
                the_index = hash(user_record.username) % self._num_buckets
                self._buckets[the_index] = user_record
                self._len += 1


    def __repr__(self):
        """Returns a string representation of the internal storage of UserMap."""
        return "\n".join(f"bucket{b}: {rec}" for b, rec in enumerate(self._buckets))

from usermap import UserMap

#Creating a UserMap instance
um = UserMap()
um.add_user("Spiderkid423", "Azeem423")

record = um["Spiderkid423"]

print(record.username)  # Output: Spiderkid423

print(record.salt)  # Output: (a random string of 5 characters)

print(record.password_hash)  # Output: (the hash of the salted password)

print(hash(record.salt + "Zeemie$"))  # Output: (the hash of the salt concatenated with "Zeemie$")
print(hash(record.salt + "Azeem423"))  # Output: (the hash of the salt concatenated with "Azeem423")
