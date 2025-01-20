## About my Project

This project is a web application that is inspired by websites like [Rotten Tomatoes](https://www.rottentomatoes.com/) and [MyAnimeList](https://myanimelist.net/) whereby it is a website that allows users to rate and review TV programs, documentaries, and all types of shows. The website also offers a community for people to engage with each other, whereby users can add Shows on the website for others to review and rate.

Users can also use this website as a watchlist. They can view the top rated shows, as well as add shows to their Favorites list.

## Distinctiveness and Complexity

My project draws upon the lessons learnt from these course and the various projects. For distinctiveness and complexity, first of all, the purpose of the website serves differently from that of a social network platform or an e-commerce platform. The website's target audience is a community of users who want to share Shows they watch online, review them, and keep track of those that they want to watch, or have watched. Distinctive features were also implemented, such as the Rating feature, whereby users can rate each show, and the show's average rating is shown. Thereby, there is also a Top Recommendations page which features the top few shows with highest average ratings. On top of such features, I utilized what I have learnt from past projects to implement features that add to the completeness of this website.

For example, the ability for Users to add a new Show. This is implemented via a POST request, and is somewhat similar to composing a new Email, writing a new social network post, creating a new Listing, or creating a new Wiki page, following something like a Create operation.

As for Update operations, Users who created a Show could edit the Synopsis (description) of that Show that they created, adding to more functionality to the website, and more power to Users who create their own Shows.

Similar to the Network project, users (logged or not logged in) are able to view profiles of other Users, or click on their own name on the Navigation to visit their own profile. However, what is distinct, is that user's profile contains the list of shows that they added to this website, and these shows are clickable links which direct them to the respective show pages.

Adding a Review in the Show is similar to adding a comment on an e-commerce listing page, but serves somewhat a difference purpose, whereby reviews are more strictly meant to be reviews (or commends) about that show. Comments on an e-commerce listing page is broader and could spark a different conversational thread, for example congratulation the winner of the bid, asking for advice on a certain item outside of the bid, and more.

The ability to toggle adding or removing a Show from Favorites is inspired by the Following/Unfollowing logic in that of a network, but in this case we are having a watchlist to a Show, while Following is the logic of a watchlist for posts from a User's profile.

To add on to distinctiveness and complexity, Users can also search for shows via the title via Partial Name Search, to filter for shows that match. The search results instantly direct the user to the same index page, but with filtered results according to the keywords. This is also different from the Wiki's project search, though inspired by it, whereby the search brings users to a "Search results" page which contains a list of navigatable links. There could also be multiple shows with the same name, therefore exact name match will not directly bring users to a specific Show's page, unlike in the Wiki project.

I also experimented the different forms of logic handling. For some features, i utilized javascript files to handle button and form logic, like rating form and editing descriptions. Whereas for Review Forms, i used form.as_p and a forms.py file, together with views.py, without a JS script to handle review logic, as learnt from the first few projects. Some views are also triggered from clicking on links on the nav bar, while some are triggered by clicking on a button on show page after adding rewviews. Therefore, I have tried severeal ways to vary my features and implementations as part of my process of learning and experimentation.


## My feature requirements
- Ability to add a new Show to Show List (set title, genre, description, image) by clicking on Add show on the navigation page, which brings u to Add Show page
- Ability to click on a show on Show List to visit Show's page
- Ability to leave a Rating in a Show in a Show page (Max 1 rating per user per show)
- Ability to leave a Review in a Show in a Show page
- Ability to toggle add/remove to Favorites List in a Show Page
- Ability to edit your own description in a Show that user created in a Show page
- Add Pagination (similar to Network)
- Show's rating is out of 5, on an average of every rating created by users
- Ability to click on a user's profile (from a comment or creator) to see their profile page, whereby profile page contains list of Shows (clickable links) the user created
- Ability to click on nav bar to visit user's OWN profile
- Search and filter shows by keyword to search for shows (similar to Wiki search)
- Top recommendations page (top 10 highest ratings)
- improvements in future iterations: Use dropdown list for Genre, refactor genre into a list of strings rather than a string itself.

## What’s contained in each file

templates/capstone
- index.html: the main page which features the list of shows. could be filtered to all shows, favorites, and by search results.
- layout.html: contains the navigation bar which will be extended by all pages.
- login.html: login page to log users in.
- register.html: page for users to register an account.
- profile.html: profile page of a user, which contains the list of Shows that a user added.
- new_show.html: A page for users to add a new Show onto the website, by specifying the Show's title, genre, synopsis, and they could also add an image_url as well.
static/capstone
- show_page.js: javascript file to handle the logic of show_page.html element interactions. Includes logic to handle User's rating via stars, and to edit the Shows' synopsis, by sending AJAX requests to the backend.
- styles.css: the style script to handle the appearance of the webpages, to beautify the app.
python files
- admin.py: to register models for superusers (admin) to access and modify.
- forms.py: contains the Review Form to write a review on a Show.
- models.py: Contains the Models that are registered in the database. Contains User, Show, Rating, and Review classes respectively.
- urls.py: Defines url patterns, and direct logic to the views.py on the backend.
- views.py: Main backbone of the backend. Handles rendering of pages, updating of Models, and all other backend operations.


## How to run the application

1. **Clone the Project Repository:**
    ```bash
    git clone https://github.com/me50/janald99.git
    cd <your_project_folder>
    ```
    At the main project directory level, you should be able to see files like manage.py, and folders like capstone and project5.

2. **Navigate to Capstone branch:**
    ```bash
    git checkout web50/projects/2020/x/capstone
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Database Migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a Superuser (Admin):**
    ```bash
    python manage.py createsuperuser
    # Follow the prompts to create a superuser account
    ```

6. **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```

7. **Access the Application:**
    Open a web browser and visit `http://127.0.0.1:8000/` to view the application.
    
7. **Access the Admin Interface:**
    - Go to `http://127.0.0.1:8000/admin/` and log in using the superuser credentials created earlier.
    - Use the Django admin interface to manage users, shows, and other data.
