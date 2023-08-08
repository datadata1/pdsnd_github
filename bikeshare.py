import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
month_input = {'all': 0,
               'january': 1,
               'february': 2,
               'march': 3,
               'april': 4,
               'may': 5,
               'june': 6}
day_input = {'all': 0, 
             'sunday': 7, 
             'monday': 1, 
             'tuesday': 2, 
             'wednesday': 3, 
             'thursday': 4, 
             'friday': 5, 
             'saturday': 6}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter

    If user enters a city, month or day outide of the expected choices, user will be prompted to try again.
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:

        try: 
            city = input('Please enter the city name you would like to get data for (i.e. chicago, new york city or washington): ')
            city = city.lower()
            CITY_DATA[city]
            break
        except KeyError:
            print('Sorry, I didn\'t get that. Please try again.')
            continue
                      
    # TO DO: get user input for month (all, january, february, ... , june)
        
    while True:    
        try: 
            month = input('Please enter a month from January through June or \'all\' for all six months (i.e. january, february, ... june, all): ')
            month = month.lower()
            month_input[month]
            break
        except KeyError:
            print('Sorry, I didn\'t get that. Please try again.')
            continue

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:    
        try: 
            day = input('Please enter a day of the week or \'all\' for the whole week (i.e. all, monday, tuesday, ... sunday): ')
            day = day.lower()
            day_input[day]
            break
        except KeyError:
            print('Sorry, I didn\'t get that. Please try again.')
            continue
    print('-'*40)
    return city.lower(), month.lower(), day.lower()


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day

    Month is converted to respective number to match the data
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe

        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # TO DO: display the most common month
    com_month = df["month"].mode()
    print("The most common month of travel is:",com_month[0])
    
    # TO DO: display the most common day of week
    com_day = df['day_of_week'].mode()
    print('The most common day of travel is:',com_day[0])

    # TO DO: display the most common start hour
    com_hour = df['hour'].mode()
    print('The most common start hour is:', com_hour[0])

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    com_start_station = df['Start Station'].mode()
    print('The most common start station is:', com_start_station[0])

    # TO DO: display most commonly used end station
    com_end_station = df['End Station'].mode()
    print('The most common end station is:', com_end_station[0])

    # TO DO: display most frequent combination of start station and end station trip
    df['Start/End'] = df['Start Station'] + "/" + df['End Station']
    com_trips = df['Start/End'].mode()
    print('The most common trip ("Start and End") is:', com_trips[0])

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel = df['Trip Duration'].sum()
    print('The total travel time is:', total_travel)

    # TO DO: display mean travel time
    avg_travel = df['Trip Duration'].mean().round()
    print('The average travel time is:', avg_travel)

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_count = df['User Type'].value_counts()
    print('The counts by user types are:\n',user_count)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('\nThe counts by gender are:\n', gender_count)
    else:
        print('\nNo Gender data available.')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth = df['Birth Year'].min()
        latest_birth = df['Birth Year'].max()
        com_birth = df['Birth Year'].mode()
        print('\nThe earliest year of birth is: {}\nThe most recent year of birth is: {}\nThe most common year of birth is: {}'.format(int(earliest_birth), int(latest_birth), int(com_birth[0])))
    else:
        print('\nNo Birth Year data available.')
    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

#Define print function
def printdata(df):
    """Displays five rows of data at a time for specified city with month and day of week filters applied."""

    while True:
        see_data = input('Would you like to see some data? ')
        see_data = see_data.lower()
        if see_data == 'no':
            break
        elif see_data == 'yes':
            print(df.head())
            row_count = len(df)
            row = 5
            while row < row_count:
                see_more = input('Would you like to see more data? ')
                see_more = see_more.lower()
                if see_more == 'no':
                    break
                elif see_more == 'yes':
                    if row + 5 > row_count:
                        print(df[row:])
                        break
                    else:
                        print(df[row:row+5])
                        row += 5
                else:
                    print('Sorry, I didn\'t get that. Please try again!')
                    continue
            break
        else:
            print('Sorry, I didn\'t get that. Please try again.')
            continue
        

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        printdata(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break



if __name__ == "__main__":
	main()
