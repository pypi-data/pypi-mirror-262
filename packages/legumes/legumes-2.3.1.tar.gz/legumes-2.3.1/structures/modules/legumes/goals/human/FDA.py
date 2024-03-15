
'''
	import legumes.goals.human.FDA as human_FDA_goal
	goal = human_FDA_goal.retrieve ()
'''

'''
	multikey index:
		https://www.mongodb.com/docs/manual/core/indexes/index-types/index-multikey/
'''
def retrieve ():
	return {
	  "label": "FDA goals for the average adult humans",
	  "cautions": [
		"These guidelines have not been checked by any high status nutritionists.",
		"Please consult with your actual physician or nutritionist also."
	  ],
	  "ingredients": [
		{
		  "labels": [
			"Biotin"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "3/100000",
				  "decimal string": "0.000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Calcium"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "13/10",
				  "decimal string": "1.300"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"calories"
		  ],
		  "goal": {
			"energy": {
			  "per Earth": {
				"food calories": {
				  "fraction string": "2000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Choline"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "11/20",
				  "decimal string": "0.550"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Cholesterol"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "3/10",
				  "decimal string": "0.300"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Chromium"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "7/200000",
				  "decimal string": "0.000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Copper"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "9/10000",
				  "decimal string": "0.001"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Dietary Fiber"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "28",
				  "decimal string": "28.000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Fats"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "78",
				  "decimal string": "78.000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Folate",
			"Folic Acid"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "1/2500",
				  "decimal string": "0.000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Iodine"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "3/20000",
				  "decimal string": "0.000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Iron"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "9/500",
				  "decimal string": "0.018"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Magnesium"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "21/50",
				  "decimal string": "0.420"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Manganese"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "23/10000",
				  "decimal string": "0.002"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Molybdenum"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "9/200000",
				  "decimal string": "0.000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Niacin"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "2/125",
				  "decimal string": "0.016"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Pantothenic Acid"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "1/200",
				  "decimal string": "0.005"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Phosphorus"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "5/4",
				  "decimal string": "1.250"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Potassium"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "47/10",
				  "decimal string": "4.700"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Protein"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "50",
				  "decimal string": "50.000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Riboflavin"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "13/10000",
				  "decimal string": "0.001"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Saturated Fat"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "20",
				  "decimal string": "20.000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Selenium"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "11/200000",
				  "decimal string": "0.000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Sodium"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "23/10",
				  "decimal string": "2.300"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Thiamin"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "3/2500",
				  "decimal string": "0.001"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"carbohydrates"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "275",
				  "decimal string": "275.000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Vitamin A"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "9/10000",
				  "decimal string": "0.001"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Vitamin B6"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "17/10000",
				  "decimal string": "0.002"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Vitamin B12"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "3/1250000",
				  "decimal string": "0.000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Vitamin C"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "9/100",
				  "decimal string": "0.090"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Vitamin D"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "1/50000",
				  "decimal string": "0.000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Vitamin E"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "3/200",
				  "decimal string": "0.015"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Vitamin K"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "3/25000",
				  "decimal string": "0.000"
				}
			  }
			}
		  }
		},
		{
		  "labels": [
			"Zinc"
		  ],
		  "goal": {
			"mass + mass equivalents": {
			  "per Earth day": {
				"grams": {
				  "fraction string": "11/1000",
				  "decimal string": "0.011"
				}
			  }
			}
		  }
		}
	  ],
	  "limiters": [
		{
		  "label": "species",
		  "includes": [
			"human"
		  ]
		},
		{
		  "kind": "slider--integer",
		  "label": "age",
		  "includes": [
			[
			  "20",
			  "eternity"
			]
		  ]
		},
		{
		  "label": "exclusions",
		  "includes": [
			"pregnant",
			"breast feeding"
		  ]
		}
	  ],
	  "sources": [
		"https://www.fda.gov/food/new-nutrition-facts-label/daily-value-new-nutrition-and-supplement-facts-labels",
		"https://www.fda.gov/food/nutrition-facts-label/calories-nutrition-facts-label",
		"https://www.fda.gov/media/99069/download",
		"https://www.fda.gov/media/99059/download"
	  ]
	}
