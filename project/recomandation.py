from random import randrange
from project.models import Review, Product
from project import db


class RecommendationGenerator:
    """
    Generates a book recommendation for user based on what he liked and what others liked
    """
    def __init__(self, user):
        self.user = user

    @staticmethod
    def build_dictionary(reviews):
        """
        Build a dictionary with the grades given by current user
        :return: dictionary : "product-id":grade
        """
        current_user_grades = dict()
        for current_user_review in reviews:
            current_user_grades[current_user_review.product_id] = current_user_review.grade
        return current_user_grades

    def compatibility_score(self, current_user_grades):
        """
        Compute the compatibility score between current_user and others,
            based on the current_user_grades
        :return: dictionary: "other_user_id": points
        """
        users_score = dict()
        for product_id, product_grade in current_user_grades.items():
            # takes the products reviewed by the current user one by one

            # look for what grades have been given by others for the current product
            reviews = Review.query.filter_by(product_id=product_id)
            for review in reviews:
                if review.author_id == self.user:
                    # check if the current review is not from current user
                    continue

                dif_between = abs(product_grade - review.grade)

                if review.author_id not in users_score.keys():
                    # if the author of current review was not added in users_score, we add him with 0 points
                    users_score[review.author_id] = 0

                users_score[review.author_id] = users_score[review.author_id] + 2 - dif_between
        return users_score

    @staticmethod
    def best_matching_persons(users_score):
        """
        Returns the persons with best matching score
        users_score: dictionary
        :return: list
        """
        best = 0
        best_persons = list()
        for person in users_score:
            if users_score[person] > best:
                best = users_score[person]
                best_persons.clear()
                best_persons.append(person)
            elif users_score[person] == best:
                best_persons.append(person)
        return best_persons

    @staticmethod
    def book_with_number_of_stars(best_persons, current_user_grades, number):
        """
        Returns all products rated with int(number) stars by persons from best_persons and not rated by current_user
        :param number: int
        :param best_persons: list
        :param current_user_grades: dictionary
        :return: list
        """
        good_products = list()
        # make the list of number stars rated products by best_persons
        for person in best_persons:
            possible_products = Review.query.filter_by(author_id=person)
            for product in possible_products:
                if product.grade == number and product.product_id not in current_user_grades.keys():
                    good_products.append(product.product_id)
        return good_products

    @staticmethod
    def get_product_with_maximum_points(current_user_grades):
        """
        Returns a product with maximum sum of grades from reviews (not rated by current user)
        :param current_user_grades: dictionary
        :return: product or -1 if there is no suitable product
        """
        products = db.session.query(Product).all()
        best = 0
        good_products = list()
        for product in products:
            if product.id not in current_user_grades.keys():
                # if current product was not rated by current user
                if int(product.points) >= best:
                    best = int(product.points)
                    good_products.clear()
                    good_products.append(product.id)
                elif int(product.points) == best:
                    good_products.append(product.id)
        if bool(good_products):
            return good_products[randrange(len(good_products))]
        return -1

    def generator(self):
        """
        Compute the recommendation
        """
        current_user_reviews = Review.query.filter_by(author_id=self.user)

        current_user_grades = self.build_dictionary(current_user_reviews)
        users_score = self.compatibility_score(current_user_grades)
        best_persons = self.best_matching_persons(users_score)

        # get all product rated with 5 stars by best matching persons
        good_products = self.book_with_number_of_stars(best_persons, current_user_grades, 5)
        # if the list is not empty, returns a random element from it
        if bool(good_products):
            return good_products[randrange(len(good_products))]

        # get all product rated with 5 stars by best matching persons
        good_products = self.book_with_number_of_stars(best_persons, current_user_grades, 4)
        # if the list is not empty, returns a random element from it
        if bool(good_products):
            return good_products[randrange(len(good_products))]

        product = self.get_product_with_maximum_points(current_user_grades)
        if product != -1:
            return product

        products = db.session.query(Product).all()
        for product in products:
            # we get here only if the current user rated all products
            # the program returns a random product
            return product.id
