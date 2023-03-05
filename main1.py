from flask import Flask, render_template, Response, request
from model import gen_frames

# Flask app code
app = Flask(__name__)

@app.route('/video_feed')
def video_feed():
    # if request.method == 'POST':
    #     data = request.get_data()
    #     #Video streaming route. Put this in the src attribute of an img tag
    #     return Response(gen_frames(data), mimetype='multipart/x-mixed-replace; boundary=frame')
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
