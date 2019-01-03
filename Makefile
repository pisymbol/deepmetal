all:
	flask run --with-threads

heroku:
	git push heroku master

slides:
	jupyter nbconvert deepmetal.ipynb --to slides --post serve --SlidesExporter.reveal_scroll=True 

.PHONY: all heroku slides
