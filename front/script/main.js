var socket = new WebSocket("ws://0.0.0.0:8000/ws");
var context;
var action = {
    up: false,
    down: false,
    left: false,
    right: false,
    shot: false
};
var last_action = {};
var send_movement = false;
var player_id = '';
window.onload = function () {
    var drawingCanvas = document.getElementById('screen');
    if (drawingCanvas && drawingCanvas.getContext) {
        context = drawingCanvas.getContext('2d');
        clean_field()
    }

    function clean_field() {
        context.fillStyle = "#2a5d64";
        context.fillRect(0, 0, drawingCanvas.width, drawingCanvas.height)

    }

    function render_main_ship(x, y, r) {
        context.fillStyle = "#b41909";
        context.save();
        context.translate(x + 3, y + 8);
        context.rotate(r * Math.PI / 180);
        context.fillRect(0, 0, 12, 32);
        context.restore();
    }

    function point(x, y, canvas) {
        context.save();
        canvas.beginPath();
        context.fillStyle = "rgb(52,251,6)";
        canvas.arc(x, y, 1, 0, 2 * Math.PI, true);
        canvas.fill();
        canvas.restore();
    }

    function render_bound_ship(x, y, r, bounds, aabb) {

        context.save();
        context.translate(x, y);
        context.rotate(r);
        var img = new Image();
        img.src = "img/main_ship.png";
        context.drawImage(img, -15, -40, 30, 100);
        context.restore();

        context.fillStyle = "rgba(133,0,5,0.61)";
        context.beginPath();
        context.moveTo(bounds[0][0], bounds[0][1]);
        bounds.forEach((elem) => {
            context.lineTo(elem[0], elem[1]);
        });
        context.fill();
        context.beginPath();
        context.rect(aabb[0], aabb[1], aabb[2] - aabb[0], aabb[3] - aabb[1]);
        context.stroke();
        point(x, y, context)
    }


    socket.onmessage = function (event) {
        let data = JSON.parse(event.data);
        if (typeof data.player_id === "string") {
            player_id = data.player_id;
        } else {
            clean_field();
            data.forEach((elem) => {
                // if (elem.id == player_id) {
                //     render_main_ship(elem.x, elem.y, elem.r);
                // } else {
                //     render_ship(elem.x, elem.y, elem.r);
                // }
                render_bound_ship(elem.x, elem.y, elem.r, elem.bounds, elem.aabb)
            });

        }
    };

    document.addEventListener('keydown', function (event) {
        evaluateMovement(event, true);
    });
    document.addEventListener('keyup', function (event) {
        evaluateMovement(event, false);
    });

    function evaluateMovement(event, action_flag) {
        switch (event.keyCode) {
            case 65: // A
                action.left = action_flag;
                break;
            case 87: // W
                action.up = action_flag;
                break;
            case 68: // D
                action.right = action_flag;
                break;
            case 83: // S
                action.down = action_flag;
                break;
            case 32: // space
                action.shot = action_flag;
                break;
        }
        if (!(last_action.up === action.up &&
            last_action.down === action.down &&
            last_action.right === action.right &&
            last_action.left === action.left &&
            last_action.shot === action.shot)) {
            for (var key in action) {
                last_action[key] = action[key];
            }
            send_movement = true;
        }
    }

    socket.onopen = function () {
        setInterval(function () {
            if (send_movement) {
                socket.send(JSON.stringify(action));
                send_movement = false;
            }
        }, 100);
    };

};
class Game {
    constructor() {
        this.socket = new WebSocket("ws://0.0.0.0:8000/ws_red");
        this.context = null;
        this.movement = {
            up: false,
            down: false,
            left: false,
            right: false
        };
        this.last_movement = {};
    }
}

