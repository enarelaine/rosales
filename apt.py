from datetime import datetime, timedelta

# Class to represent an appointment
class Appointment:
    def __init__(self, owner_name, contact_number, guests, duration, target_date):
        """ Initializes an Appointment object with the given details."""
        self.owner_name = owner_name  # Name of the person booking
        self.contact_number = contact_number  # Contact number of the person booking
        self.guests = guests  # Number of guests
        self.duration = duration  # Length of stay in days
        self.target_date = target_date  # Start date of the stay (arrival date)

    def calculate_departure_date(self):
        """ Calculates the departure date based on the target_date and duration of the stay. Returns the departure date in MM/DD/YYYY format. """
        arrival_date = datetime.strptime(self.target_date, '%m/%d/%Y')  # Convert target_date to datetime
        departure_date = arrival_date + timedelta(days=self.duration)  # Add duration to calculate departure date
        return departure_date.strftime('%m/%d/%Y')  # Format the departure date as a string

    def get_stay_dates(self):
        """Returns a list of all dates for the stay period, from arrival to departure."""
        arrival_date = datetime.strptime(self.target_date, '%m/%d/%Y')  # Convert target_date to datetime
        # Generate list of stay dates
        return [(arrival_date + timedelta(days=i)).strftime('%m/%d/%Y') for i in range(self.duration)]


# List to store all appointment objects
appointments = []

def is_date_available(target_date, duration):
    """Checks if the requested stay period overlaps with any existing appointments. Returns True if the date range is available, otherwise False. """
    # Generate the list of requested stay dates
    requested_dates = [(datetime.strptime(target_date, '%m/%d/%Y') + timedelta(days=i)).strftime('%m/%d/%Y') 
                       for i in range(duration)]
    
    # Check each existing appointment for overlap
    for appointment in appointments:
        if any(date in appointment.get_stay_dates() for date in requested_dates):
            return False  # Conflict found, date is not available
    return True  # No conflict, date is available

def make_appointment():
    """ Handles the process of making a new appointment.Includes validation for user inputs and checks for date availability."""
    owner_name = input("Enter your name: ")  # Collect owner's name
    contact_number = input("Enter your contact number: ")  # Collect contact number
    
    try:
        # Collect number of guests and validate the input
        guests = int(input("Enter the number of guests: "))
        if guests <= 0:
            raise ValueError("Number of guests must be a positive integer.")
        
        # Collect the duration of the stay and validate the input
        duration = int(input("Enter the length of stay (in days): "))
        if duration <= 0:
            raise ValueError("Duration must be a positive integer.")
        
        # Continuously prompt for a valid and available target date
        while True:
            target_date = input("Enter your target date (MM/DD/YYYY): ")
            try:
                datetime.strptime(target_date, '%m/%d/%Y')  # Validate date format
                if is_date_available(target_date, duration):  # Check availability
                    break  # Exit loop if date is valid and available
                else:
                    print("The date range is not available. Please choose another start date.")
            except ValueError:
                print("Invalid date format. Please use MM/DD/YYYY.")
        
        # Create and store the appointment
        appointment = Appointment(owner_name, contact_number, guests, duration, target_date)
        appointments.append(appointment)  # Add to global list
        # Display confirmation
        print("\n------Appointment Scheduled------")
        print(f"Name: {appointment.owner_name}")
        print(f"Contact Number: {appointment.contact_number}")
        print(f"Guests: {appointment.guests}")
        print(f"Length of Stay: {appointment.duration} days")
        print(f"Arrival Date: {appointment.target_date}")
        print(f"Departure Date: {appointment.calculate_departure_date()}")
        
    except ValueError as ve:
        # Handle invalid inputs
        print(f"Error: {ve}. Please try again.")

def view_appointments():
    """  Displays all existing appointments with details including booked dates. """
    if not appointments:
        print("No appointments have been made yet.")  # Inform if no appointments exist
        return
    
    print("\n------All Appointments------")
    # Iterate through the list of appointments
    for i, appt in enumerate(appointments, 1):
        print(f"\nAppointment {i}:")
        print(f"Name: {appt.owner_name}")
        print(f"Contact Number: {appt.contact_number}")
        print(f"Guests: {appt.guests}")
        print(f"Length of Stay: {appt.duration} days")
        print(f"Arrival Date: {appt.target_date}")
        print(f"Departure Date: {appt.calculate_departure_date()}")
        print(f"Booked Dates: {', '.join(appt.get_stay_dates())}")  # Show all booked dates

def main():
    """  Main function to control the flow of the application. Allows users to choose between admin and user roles.` """
    print("Welcome to the Airbnb Planning and Tracking System!\n")
    
    while True:
        try:
            # Prompt for role selection
            role = input("Are you an Admin or User? (Enter 'admin' or 'user'): ").strip().lower()
            
            if role == "admin":
                print("\n------Admin Section------")
                view_appointments()  # Admin views all appointments
            elif role == "user":
                print("\n------User Section------")
                make_appointment()  # User creates a new appointment
            else:
                print("Invalid role. Please enter 'admin' or 'user'.")
                continue  # Prompt again for a valid role
            
            # Ask if the user wants to continue or exit
            another = input("\nWould you like to continue? (yes/no): ").strip().lower()
            if another not in ['yes', 'no']:
                raise ValueError("Please enter 'yes' or 'no'.")  # Validate input
            
            if another != 'yes':
                break  # Exit the loop if the user doesn't want to continue
        except ValueError as ve:
            # Handle invalid inputs
            print(f"Error: {ve}. Please try again.")

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()
