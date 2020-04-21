import time
import pandas as pd
import numpy as np


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington)
    city_filter_list = ['chicago', 'new york city', 'washington']
    while True:
        city = input('Enter the name of a valid city (Chicago, New York City, Washington): ').strip()
        if city.lower() not in city_filter_list:
            print('That is not a valid city. Enter either Chicago, New York, or Washington')
        else:
            city = city.lower().replace(' ', '_')
            break

    choice_list = ['month', 'day', 'neither']
    while True:
        choice = input('Would you like to filter the data by month, day,or neither? ').strip()
        if choice.lower() not in choice_list:
            print('That is not a valid choice. Enter month, day, or neither')
        else:
            choice = choice.lower()
            break

    if choice == 'month':
        # get user input for month (all, january, february, ... , june)
        month_filter_list = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        while True:
            month = input ('Enter a month: ').strip()
            if month.lower() not in month_filter_list:
                print('That is not a valid month entry')
            else:
                month = month.lower()
                break
    else:
        month = 'all'

    if choice == 'day':
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day_of_week_filter_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        while True:
            day = input ('Enter a specific day: ').strip()
            if day.lower() not in day_of_week_filter_list:
                print('That is not a valid day entry')
            else:
                day = day.lower()
                break
    else:
        day = 'all'

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(city + '.csv')

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'], yearfirst=True)

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
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

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    print('The most common month to travel: {}'.format(months[df['month'].mode()[0] - 1].title()))

    # display the most common day of week
    print('The most common day of the week to travel: {}'.format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    print('The most common start hour: {}'.format(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station: {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('The most commonly used end station: {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    freq_combo = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('The most frequent combination of start station and end station trip are:\n\tStart:\t{}\n\tEnd:\t{}'.format(freq_combo[0], freq_combo[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time was {}'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('The average time traveled was {}'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    print('User types and counts')
    for user_type, user_count in df['User Type'].value_counts().iteritems():
        print('\t' + user_type + ': ' + str(user_count))

    if  'Gender' in df:
        print()
        # display counts of gender
        print('Gender and counts')
        for gender, gender_count in df['Gender'].value_counts().iteritems():
            print('\t' + gender + ': ' + str(gender_count))
        print()

    if 'Birth Year' in df:
        # display earliest, most recent, and most common year of birth
        print('The most recent year of birth: {}'.format(df['Birth Year'].max()))
        print('The earliest year of birth: {}'.format(df['Birth Year'].min()))
        print('The most common year of birth: {}'.format(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw DataFrame data if user wishes."""

    # counter used to keep track of rows displayed
    counter = 0
    while True:
        choice = input('Would you like to see raw data? (Yes or No): ').strip()
        if choice.lower() == 'no':
            break
        elif choice.lower() != 'yes':
            print('Not a valid choice')
            continue

        # print slice of 5 dataframe rows at a time
        print(df.iloc[counter:counter+5])
        counter+=5


def main():

    # Loops until user quits
    while True:
        # Get input from users and create a DataFrame
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        # Display information to the user
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
