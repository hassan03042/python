import requests
import json
import random
from typing import List, Dict

API_KEY = "YOUR_SPOONACULAR_API_KEY"  # Replace with your actual API key
BASE_URL = "https://api.spoonacular.com/recipes"

class Recipe:
    def __init__(self, id: int, title: str, image: str):
        self.id = id
        self.title = title
        self.image = image

class RecipeApp:
    def __init__(self):
        self.favorites: List[Recipe] = []
        self.load_favorites()

    def search_recipes(self, query: str, diet: str = None, cuisine: str = None) -> List[Recipe]:
        params = {
            "apiKey": API_KEY,
            "query": query,
            "number": 10
        }
        if diet:
            params["diet"] = diet
        if cuisine:
            params["cuisine"] = cuisine

        response = requests.get(f"{BASE_URL}/complexSearch", params=params)
        data = response.json()
        return [Recipe(r["id"], r["title"], r["image"]) for r in data["results"]]

    def get_recipe_details(self, recipe_id: int) -> Dict:
        params = {"apiKey": API_KEY}
        response = requests.get(f"{BASE_URL}/{recipe_id}/information", params=params)
        return response.json()

    def add_favorite(self, recipe: Recipe):
        if recipe not in self.favorites:
            self.favorites.append(recipe)
            self.save_favorites()
            print(f"Added {recipe.title} to favorites.")
        else:
            print("Recipe already in favorites.")

    def remove_favorite(self, recipe_id: int):
        self.favorites = [r for r in self.favorites if r.id != recipe_id]
        self.save_favorites()
        print("Recipe removed from favorites.")

    def save_favorites(self):
        with open("favorites.json", "w") as f:
            json.dump([r.__dict__ for r in self.favorites], f)

    def load_favorites(self):
        try:
            with open("favorites.json", "r") as f:
                data = json.load(f)
                self.favorites = [Recipe(**r) for r in data]
        except FileNotFoundError:
            self.favorites = []

    def generate_meal_plan(self, num_meals: int, diet: str = None) -> List[Recipe]:
        params = {
            "apiKey": API_KEY,
            "timeFrame": "day",
            "targetCalories": 2000,
            "number": num_meals
        }
        if diet:
            params["diet"] = diet

        response = requests.get(f"{BASE_URL}/mealplanner/generate", params=params)
        data = response.json()
        return [Recipe(meal["id"], meal["title"], "") for meal in data["meals"]]

def main():
    app = RecipeApp()

    while True:
        print("\n--- Advanced Food Recipe App ---")
        print("1. Search Recipes")
        print("2. View Recipe Details")
        print("3. Add to Favorites")
        print("4. View Favorites")
        print("5. Remove from Favorites")
        print("6. Generate Meal Plan")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            query = input("Enter search query: ")
            diet = input("Enter diet (optional): ")
            cuisine = input("Enter cuisine (optional): ")
            recipes = app.search_recipes(query, diet, cuisine)
            for i, recipe in enumerate(recipes, 1):
                print(f"{i}. {recipe.title}")

        elif choice == "2":
            recipe_id = int(input("Enter recipe ID: "))
            details = app.get_recipe_details(recipe_id)
            print(f"\nTitle: {details['title']}")
            print(f"Ready in: {details['readyInMinutes']} minutes")
            print(f"Servings: {details['servings']}")
            print("Ingredients:")
            for ingredient in details['extendedIngredients']:
                print(f"- {ingredient['original']}")
            print("\nInstructions:")
            for step in details['analyzedInstructions'][0]['steps']:
                print(f"{step['number']}. {step['step']}")

        elif choice == "3":
            recipe_id = int(input("Enter recipe ID to add to favorites: "))
            details = app.get_recipe_details(recipe_id)
            recipe = Recipe(details['id'], details['title'], details['image'])
            app.add_favorite(recipe)

        elif choice == "4":
            print("\nFavorites:")
            for i, recipe in enumerate(app.favorites, 1):
                print(f"{i}. {recipe.title}")

        elif choice == "5":
            recipe_id = int(input("Enter recipe ID to remove from favorites: "))
            app.remove_favorite(recipe_id)

        elif choice == "6":
            num_meals = int(input("Enter number of meals: "))
            diet = input("Enter diet (optional): ")
            meal_plan = app.generate_meal_plan(num_meals, diet)
            print("\nGenerated Meal Plan:")
            for i, meal in enumerate(meal_plan, 1):
                print(f"{i}. {meal.title}")

        elif choice == "7":
            print("Thank you for using the Advanced Food Recipe App. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

# Example usage:
# python recipe_app.py