from project import db
from project.models import Review, Product
from project.recomandation import RecommendationGenerator
from flask import render_template, Blueprint, request
from flask_login import login_required, current_user
from project.home.form import MessageForm

home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)


# use decorators to link the function to a url
@home_blueprint.route('/', methods=['GET', 'POST'])  # pragma: no cover
@login_required
def home():
    def match(string1, string2):
        """
        Check if string1 and string2 have similarities
        :param string1: string
        :param string2: string
        :return: bool
        """
        string1 = string1.lower()
        string2 = string2.lower()
        words = string1.split()
        for word in words:
            if word in string2:
                return True
        words2 = string2.split()
        for word in words2:
            if word in string1:
                return True
        return False

    def get_last_15_reviews():
        """
        Returns the last 15 reviews from the database
        """
        latest_reviews = db.session.query(Review).all()
        latest_reviews.reverse()
        while len(latest_reviews) > 15:
            latest_reviews.pop()
        return latest_reviews

    error = None
    form = MessageForm(request.form)

    product_for_review = db.session.query(Product).get(0)

    empty_list = []
    recommendation = 0
    if form.validate_on_submit():
        # a button was pressed
        if "make_recommendation" in request.form:
            # make_recommendation button was pressed, so we have to generate a recommendation and display the result
            recommendation = db.session.query(Product).get(RecommendationGenerator(current_user.id).generator())
            reviews = get_last_15_reviews()
            return render_template('index.html', posts=reviews, finded=empty_list, form=form, error=error,
                                   product=product_for_review, stars=int(0), recommendation=recommendation)

        if "add_review_button" in request.form:
            # add_review_button was pressed, so the program should take the review from the user and add it in db
            posts = db.session.query(Review).all()
            stars_number, products_id = str(request.form['add_review_button']).split('.')

            # check if there was a review from that user for that product in the past
            to_add = True
            for post in posts:
                if int(post.author_id) == int(current_user.id) and int(post.product_id) == int(products_id):
                    to_add = False

            # if the current user has not added any product reviews, he can add now
            if to_add:
                review = Review(
                    author=current_user.id,
                    product=int(products_id),
                    grade=int(stars_number)
                )
                db.session.add(review)
                db.session.commit()
            reviews = get_last_15_reviews()
            return render_template('index.html', posts=reviews, finded=empty_list, form=form, error=error,
                                   product=product_for_review, stars=int(stars_number),
                                   recommendation=recommendation)

        if "search_button" in request.form:
            # if the current user pressed search_button, we take the content of the search box
            # and search for similarities in title/author/year of products from database
            products_list = []
            products = db.session.query(Product).all()
            title = str(form.search.data)
            author = str(form.search.data)
            year = str(form.search.data)

            if title == '':
                # if the search box is empty, we display all products
                products_list = products
            else:
                for product in products:
                    # take products one by one from database and check for similarities
                    if title != '.' and match(title, product.name):
                        products_list.append(product)
                    elif author != '.' and match(author, product.author):
                        products_list.append(product)
                    elif year != '.' and match(year, product.year):
                        products_list.append(product)
            reviews = get_last_15_reviews()
            return render_template('index.html', posts=reviews, finded=products_list, form=form, error=error,
                                   product=product_for_review, stars=int(0),
                                   recommendation=recommendation)

        stars_number = 0
        if "stars" not in request.form:
            # that part take the id of chosen product from user
            product_id = request.form['choose']
        else:
            # that part changes the number of stars for a product, according to what the user chose
            stars_number, product_id = str(request.form['stars']).split('.')

        # the program displays the product chosen for review and the current number of stars
        product_for_review = db.session.query(Product).get(product_id)
        reviews = get_last_15_reviews()
        return render_template('index.html', posts=reviews, finded=empty_list, form=form, error=error,
                               product=product_for_review, stars=int(stars_number),
                               recommendation=recommendation)

    else:
        # no button has been pressed so far
        reviews = get_last_15_reviews()
        return render_template('index.html', posts=reviews, finded=empty_list, form=form, error=error,
                               product=product_for_review, stars=int(0), recommendation=recommendation)
