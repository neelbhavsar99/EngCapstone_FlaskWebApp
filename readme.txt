Flask Web Application for Computer Vision




// To setup, run application
    1) Open VSCode, create a virtual environment
    2) Open built-in terminal, install the libraries using requirements.txt
    3) python3 app.py (it will start the development server)


Harcascades -> used for facial detection (eyes and face)
// https://medium.com/analytics-vidhya/haar-cascades-explained-38210e57970d

-> It is a ML object detection algorithm to identify objects with the following steps
    1) Haar Feature Selection (face,nose,eyebrows, etc.)
        - edge feature, line features, four-rectangle features
        - pixels taken and only some will go to next stage
        - summing the pixel intensities in each region and calculating the differences between the sums
    2) Creating integral Images
        - Instead of computing at every pixel, it instead creates sub-rectangles and creates array references for each of those sub-rectangles
    3) Adaboost Training
        - decisions for splitting the correctly classified part of the Images
        - give weightage (positive-negative) based on correct-incorrect subimages
    4) Cascading Classifiers
        - three stages combined, turns weak learners to strong learners

The XML files are for detecting various object features
