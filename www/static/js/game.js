class Particle {
    constructor(game) {
        this.game = game;
        this.markedForDeletion = false;
    }
    update() {
        this.x -= this.speedX + this.game.speed;
        this.y -= this.speedY;
        this.size *= 0.95;
        if (this.size < 0.5) this.markedForDeletion = true;
    }
}
class Dust extends Particle {
    constructor(game, x, y) {
        super(game);
        this.size = Math.random() * 10 + 10;
        this.x = x;
        this.y = y;
        this.speedX = Math.random();
        this.speedY = Math.random();
        this.color = "rgba(0,0,0,0.5)";
    }
    draw(context) {
        context.beginPath();
        context.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        context.fillStyle = this.color;
        context.fill();
    }
}
class Fire extends Particle {
    constructor(game, x, y) {
        super(game);
        this.image = document.getElementById("fire");
        this.size = Math.random() * 100 + 50;
        this.x = x;
        this.y = y;
        this.speedX = 1;
        this.speedY = 1;
        this.angel = 0;
        this.va = Math.random() * 0.2 - 0.1;
    }
    update() {
        super.update();
        this.angel += this.va;
        this.x += Math.sin(this.angel * 10);
    }
    draw(context) {
        context.save();
        context.translate(this.x, this.y);
        context.rotate(this.angel);
        context.drawImage(
            this.image,
            -this.size * 0.5,
            -this.size * 0.5,
            this.size,
            this.size
        );
        context.restore();
    }
}
class Splash extends Particle {
    constructor(game, x, y) {
        super(game);
        this.size = Math.random() * 100 + 100;
        this.x = x - this.size * 0.4;
        this.y = y - this.size * 0.5;
        this.speedX = Math.random() * 6 - 4;
        this.speedY = Math.random() * 2 + 1;
        this.gravity = 0;
        this.image = document.getElementById("fire");
    }
    update() {
        super.update();
        this.gravity += 0.1;
        this.y += this.gravity;
    }
    draw(context) {
        context.drawImage(this.image, this.x, this.y, this.size, this.size);
    }
}
const states = {
    SITTING: 0,
    RUNNING: 1,
    JUMPING: 2,
    FALLING: 3,
    ROLLING: 4,
    DIVING: 5,
    HIT: 6,
};
class State {
    constructor(state, game) {
        this.state = state;
        this.game = game;
    }
}
class Sitting extends State {
    constructor(game) {
        super("SITTING", game);
    }
    enter() {
        this.game.player.frameX = 0;
        this.game.player.frameY = 5;
        this.game.player.maxFrame = 4;
    }
    handleInput(input) {
        if (input.includes("ArrowLeft") || input.includes("ArrowRight")) {
            this.game.player.setState(states.RUNNING, 1);
        } else if (input.includes(" ")) {
            this.game.player.setState(states.ROLLING, 2);
        }
    }
}
class Running extends State {
    constructor(game) {
        super("RUNNING", game);
    }
    enter() {
        this.game.player.frameX = 0;
        this.game.player.frameY = 3;
        this.game.player.maxFrame = 8;
    }
    handleInput(input) {
        this.game.particles.unshift(
            new Dust(
                this.game,
                this.game.player.x + this.game.player.width * 0.5,
                this.game.player.y + this.game.player.height
            )
        );
        if (input.includes("ArrowDown")) {
            this.game.player.setState(states.SITTING, 0);
        } else if (input.includes("ArrowUp")) {
            this.game.player.setState(states.JUMPING, 1);
        } else if (input.includes(" ")) {
            this.game.player.setState(states.ROLLING, 2);
        }
    }
}
class Jumping extends State {
    constructor(game) {
        super("JUMPING", game);
    }
    enter() {
        if (this.game.player.onGround()) this.game.player.vy -= 30;
        this.game.player.frameX = 0;
        this.game.player.frameY = 1;
        this.game.player.maxFrame = 6;
    }
    handleInput() {
        if (this.game.player.onGround())
            this.game.player.setState(states.RUNNING, 1);
        else if (!this.game.player.onGround())
            this.game.player.setState(states.FALLING, 1);
        else if (input.includes(" ")) {
            this.game.player.setState(states.ROLLING, 2);
        } else if (input.includes("ArrowDown")) {
            this.game.player.setState(states.DIVING, 0);
        }
    }
}
class Falling extends State {
    constructor(game) {
        super("FALLING", game);
    }
    enter() {
        this.game.player.frameX = 0;
        this.game.player.frameY = 2;
        this.game.player.maxFrame = 6;
    }
    handleInput(input) {
        if (this.game.player.onGround()) {
            this.game.player.setState(states.RUNNING, 1);
        } else if (input.includes("ArrowDown")) {
            this.game.player.setState(states.DIVING, 0);
        }
    }
}
class Rolling extends State {
    constructor(game) {
        super("ROLLING", game);
    }
    enter() {
        this.game.player.frameX = 0;
        this.game.player.frameY = 6;
        this.game.player.maxFrame = 6;
    }
    handleInput(input) {
        this.game.particles.unshift(
            new Fire(
                this.game,
                this.game.player.x + this.game.player.width * 0.5,
                this.game.player.y + this.game.player.height * 0.5
            )
        );
        if (!input.includes(" ") && this.game.player.onGround()) {
            this.game.player.setState(states.RUNNING, 1);
        } else if (!input.includes(" ") && !this.game.player.onGround()) {
            this.game.player.setState(states.FALLING, 1);
        } else if (
            input.includes(" ") &&
            input.includes("ArrowUp") &&
            this.game.player.onGround()
        ) {
            this.game.player.vy -= 27;
        } else if (
            input.includes("ArrowDown") &&
            !this.game.player.onGround()
        ) {
            this.game.player.setState(states.DIVING, 0);
        }
    }
}
class Diving extends State {
    constructor(game) {
        super("Diving", game);
    }
    enter() {
        this.game.player.frameX = 0;
        this.game.player.frameY = 6;
        this.game.player.maxFrame = 6;
        this.game.player.vy = 15;
    }
    handleInput(input) {
        this.game.particles.unshift(
            new Fire(
                this.game,
                this.game.player.x + this.game.player.width * 0.5,
                this.game.player.y + this.game.player.height * 0.5
            )
        );
        if (this.game.player.onGround()) {
            this.game.player.setState(states.RUNNING, 1);
            for (let i = 0; i < 30; i++) {
                this.game.particles.unshift(
                    new Splash(
                        this.game,
                        this.game.player.x + this.game.player.width * 0.5,
                        this.game.player.y + this.game.player.height
                    )
                );
            }
        } else if (input.includes(" ") && this.game.player.onGround()) {
            this.game.player.setState(states.ROLLING, 2);
        }
    }
}
class Hit extends State {
    constructor(game) {
        super("Hit", game);
    }
    enter() {
        this.game.player.frameX = 0;
        this.game.player.frameY = 4;
        this.game.player.maxFrame = 10;
    }
    handleInput(input) {
        if (this.game.player.frameX >= 10 && this.game.player.onGround()) {
            this.game.player.setState(states.RUNNING, 1);
        } else if (
            this.game.player.frameX >= 10 &&
            !this.game.player.onGround()
        ) {
            this.game.player.setState(states.FALLING, 1);
        }
    }
}
class CollisionAnimation {
    constructor(game, x, y) {
        this.game = game;
        this.image = document.getElementById("collisionAnimation");
        this.spritWidth = 100;
        this.spritHeight = 90;
        this.sizeModifier = Math.random() + 0.5;
        this.width = this.sizeModifier * this.spritWidth;
        this.height = this.sizeModifier * this.spritHeight;
        this.x = x - this.width * 0.5;
        this.y = y - this.height * 0.5;
        this.frameX = 0;
        this.maxFrame = 4;
        this.markedForDeletion = false;
        this.fps = Math.random() * 10 + 5;
        this.frameInterval = 1000 / this.fps;
        this.frameTimer = 0;
        this.audio = iceattack;
        this.audio.volume = 0.6
    }
    draw(context) {
        if(this.frameX === 0) {
            this.audio.currentTime = 0;
            this.audio.play();
        }
        context.drawImage(
            this.image,
            this.frameX * this.spritWidth,
            0,
            this.spritWidth,
            this.spritHeight,
            this.x,
            this.y,
            this.width,
            this.height
        );
    }
    update(deltaTime) {
        this.x -= this.game.speed;
        if (this.frameTimer > this.frameInterval) {
            this.frameX++;
            this.frameTimer = 0;
        } else {
            this.frameTimer += deltaTime;
        }
        if (this.frameX > this.maxFrame) {
            this.markedForDeletion = true;
        }
    }
}
class FloatingMessage {
    constructor(value, x, y, targetX, targetY) {
        this.value = value;
        this.x = x;
        this.y = y;
        this.targetX = targetX;
        this.targetY = targetY;
        this.markedForDeletion = false;
        this.timer = 0;
    }
    update() {
        this.x += (this.targetX - this.x) * 0.03;
        this.y += (this.targetY - this.y) * 0.03;
        this.timer++;
        if (this.timer > 100) {
            this.markedForDeletion = true;
        }
    }
    draw(context) {
        context.font = "20px Creepster";
        context.fillStyle = "white";
        context.fillText(this.value, this.x, this.y);
        context.fillStyle = "black";
        context.fillText(this.value, this.x - 2, this.y - 2);
    }
}
class Player {
    constructor(game) {
        this.game = game;
        this.width = 100;
        this.height = 91.3;
        this.x = 0;
        this.y = this.game.height - this.height - this.game.groundMargin;
        this.vy = 0;
        this.weight = 1;
        this.image = document.getElementById("player");
        this.frameX = 0;
        this.maxFrame = 5;
        this.fps = 20;
        this.frameInterval = 1000 / this.fps;
        this.frameTimer = 0;
        this.frameY = 0;
        this.speed = 0;
        this.maxSpeed = 10;
        this.states = [
            new Sitting(this.game),
            new Running(this.game),
            new Jumping(this.game),
            new Falling(this.game),
            new Rolling(this.game),
            new Diving(this.game),
            new Hit(this.game),
        ];
        this.currentState = null;
    }
    update(input, deltaTime) {
        this.checkCollision();
        this.currentState.handleInput(input);
        // 水平移动
        this.x += this.speed;
        if (
            input.includes("ArrowRight") &&
            this.currentState !== this.states[6]
        )
            this.speed = this.maxSpeed;
        else if (
            input.includes("ArrowLeft") &&
            this.currentState !== this.states[6]
        )
            this.speed = -this.maxSpeed;
        else this.speed = 0;
        // 限制玩家不超过水平画布
        if (this.x < 0) this.x = 0;
        if (this.x > this.game.width - this.width)
            this.x = this.game.width - this.width;
        // 垂直距离
        this.y += this.vy;
        if (!this.onGround()) this.vy += this.weight;
        else this.vy = 0;
        // 限制玩家不超过垂直画布
        if (this.y > this.game.height - this.height - this.game.groundMargin) {
            this.y = this.game.height - this.height - this.game.groundMargin;
        }
        // 动画部分
        if (this.frameTimer > this.frameInterval) {
            this.frameTimer = 0;
            if (this.frameX < this.maxFrame) this.frameX++;
            else this.frameX = 0;
        } else {
            this.frameTimer += deltaTime;
        }
    }
    draw(context) {
        if (this.game.debug) {
            context.strokeRect(this.x, this.y, this.width, this.height);
        }
        context.drawImage(
            this.image,
            this.frameX * this.width,
            this.frameY * this.height,
            this.width,
            this.height,
            this.x,
            this.y,
            this.width,
            this.height
        );
    }
    onGround() {
        return (
            this.y >= this.game.height - this.height - this.game.groundMargin
        );
    }
    setState(state, speed) {
        this.currentState = this.states[state];
        this.game.speed = this.game.maxSpeed * speed;
        this.currentState.enter();
    }
    checkCollision() {
        this.game.enemies.forEach((enemy) => {
            if (
                enemy.x < this.x + this.width &&
                enemy.x + enemy.width > this.x &&
                enemy.y < this.y + this.height &&
                enemy.y + enemy.height > this.y
            ) {
                //发生碰撞
                enemy.markedForDeletion = true;
                this.game.collisions.push(
                    new CollisionAnimation(
                        this.game,
                        enemy.x + enemy.width * 0.5,
                        enemy.y + enemy.height * 0.5
                    )
                );
                if (
                    this.currentState === this.states[4] ||
                    this.currentState === this.states[5]
                ) {
                    this.game.score++;
                    this.game.floatingMessages.push(
                        new FloatingMessage("+1", enemy.x, enemy.y, 150, 50)
                    );
                } else {
                    this.setState(6, 0);
                    this.game.score -= 5;
                    this.game.lives--;
                    if (this.game.lives <= 0) this.game.gameOver = true;
                }
            }
        });
    }
}
class InputHandler {
    constructor(game) {
        this.game = game;
        this.keys = [];
        // this.bindEvent();
    }
    bindEvent() {
        window.addEventListener("keydown", (e) => {
            if (
                (e.key === "ArrowDown" ||
                    e.key === "ArrowUp" ||
                    e.key === "ArrowLeft" ||
                    e.key === "ArrowRight" ||
                    e.key === " ") &&
                this.keys.indexOf(e.key) === -1
            ) {
                this.keys.push(e.key);
            } else if (e.key === "d") {
                this.game.debug = !this.game.debug;
            }
        });
        window.addEventListener("keyup", (e) => {
            if (
                e.key === "ArrowDown" ||
                e.key === "ArrowUp" ||
                e.key === "ArrowLeft" ||
                e.key === "ArrowRight" ||
                e.key === " "
            ) {
                this.keys.splice(this.keys.indexOf(e.key), 1);
            }
        });
    }
}
class Layer {
    constructor(game, width, height, speedModifier, image) {
        this.game = game;
        this.width = width;
        this.height = height;
        this.speedModifier = speedModifier;
        this.image = image;
        this.x = 0;
        this.y = 0;
    }
    update() {
        if (this.x < -this.width) this.x = 0;
        else this.x -= this.game.speed * this.speedModifier;
    }
    draw(context) {
        context.drawImage(this.image, this.x, this.y, this.width, this.height);
        context.drawImage(
            this.image,
            this.x + this.width,
            this.y,
            this.width,
            this.height
        );
    }
}
class BackGround {
    constructor(game) {
        this.game = game;
        // this.width = 1667;
        // this.height = 500;
        this.width = window.innerWidth;
        this.height = window.innerHeight;
        this.layerImage1 = document.getElementById("layer1");
        this.layerImage2 = document.getElementById("layer2");
        this.layerImage3 = document.getElementById("layer3");
        this.layerImage4 = document.getElementById("layer4");
        this.layerImage5 = document.getElementById("layer5");
        this.layer1 = new Layer(
            this.game,
            this.width,
            this.height,
            0,
            this.layerImage1
        );
        this.layer2 = new Layer(
            this.game,
            this.width,
            this.height,
            0.2,
            this.layerImage2
        );
        this.layer3 = new Layer(
            this.game,
            this.width,
            this.height,
            0.4,
            this.layerImage3
        );
        this.layer4 = new Layer(
            this.game,
            this.width,
            this.height,
            0.6,
            this.layerImage4
        );
        this.layer5 = new Layer(
            this.game,
            this.width,
            this.height,
            0.8,
            this.layerImage5
        );
        this.BackGroundLayers = [
            this.layer1,
            this.layer2,
            this.layer3,
            this.layer4,
            this.layer5,
        ];
    }
    update() {
        this.BackGroundLayers.forEach((layer) => {
            layer.update();
        });
    }
    draw(context) {
        this.BackGroundLayers.forEach((layer) => {
            layer.draw(context);
        });
    }
}
class Enemy {
    constructor() {
        this.frameX = 0;
        this.frameY = 0;
        this.fps = 20;
        this.frameInterval = 1000 / this.fps;
        this.frameTimer = 0;
        this.markedForDeletion = false;
    }
    update(deltaTime) {
        this.x -= this.speedX + this.game.speed;
        this.y += this.speedY;
        if (this.frameTimer > this.frameInterval) {
            this.frameTimer = 0;
            if (this.frameX < this.maxFrame) this.frameX++;
            else this.frameX = 0;
        } else {
            this.frameTimer += deltaTime;
        }
        // 对敌人进行检查，超过屏幕就进行删除
        if (this.x + this.width < 0) this.markedForDeletion = true;
    }
    draw(context) {
        if (this.game.debug) {
            context.strokeRect(this.x, this.y, this.width, this.height);
        }
        context.drawImage(
            this.image,
            this.frameX * this.width,
            0,
            this.width,
            this.height,
            this.x,
            this.y,
            this.width,
            this.height
        );
    }
}
class FlyingEnemy extends Enemy {
    constructor(game) {
        super();
        this.game = game;
        this.width = 60;
        this.height = 44;
        this.x = this.game.width;
        this.y = Math.random() * this.game.height * 0.5;
        this.speedX = Math.random() + 1;
        this.speedY = 0;
        this.maxFrame = 5;
        this.image = document.getElementById("enemy_fly");
        this.angle = 0;
        this.va = Math.random() * 0.1 + 0.1;
    }
    update(deltaTime) {
        super.update(deltaTime);
        this.angle += this.va;
        this.y += Math.sin(this.angle);
    }
}
class GroundEnemy extends Enemy {
    constructor(game) {
        super();
        this.game = game;
        this.width = 60;
        this.height = 87;
        this.x = this.game.width;
        this.y = this.game.height - this.height - this.game.groundMargin;
        this.speedX = 0;
        this.speedY = 0;
        this.maxFrame = 1;
        this.image = document.getElementById("enemy_plant");
    }
}
class ClimbingEnemy extends Enemy {
    constructor(game) {
        super();
        this.game = game;
        this.width = 120;
        this.height = 144;
        this.x = this.game.width;
        this.y = Math.random() * this.game.height * 0.5;
        this.image = document.getElementById("enemy_spider_big");
        this.speedX = 0;
        this.speedY = Math.random() > 0.5 ? 1 : -1;
        this.maxFrame = 5;
    }
    update(deltaTime) {
        super.update(deltaTime);
        if (this.y > this.game.height - this.height - this.game.groundMargin)
            this.speedY *= -1;
        if (this.y < -this.height) this.markedForDeletion = true;
    }
    draw(context) {
        super.draw(context);
        context.beginPath();
        context.moveTo(this.x + this.width / 2, 0);
        context.lineTo(this.x + this.width / 2, this.y);
        context.stroke();
    }
}
class UI {
    constructor(game) {
        this.game = game;
        this.fontSize = 28;
        this.fontFamily = "Creepster";
        this.liveImage = document.getElementById("lives");
    }
    draw(context) {
        context.save();
        context.font = this.fontSize + "px " + this.fontFamily;
        context.textAlign = "left";
        context.fillStyle = this.game.fontColor;
        // 分数绘制
        context.fillText("分数: " + this.game.score, 20, 50);
        // 时间绘制
        context.font = this.fontSize * 0.8 + "px " + this.fontFamily;
        context.fillText(
            "时长: " + (this.game.time * 0.001).toFixed(1),
            20,
            80
        );
        // 生命值绘制
        for (let i = 0; i < this.game.lives; i++) {
            context.drawImage(this.liveImage, 25 * i + 20, 95, 25, 25);
        }
        // 游戏结束看板
        if (this.game.gameOver) {
            // context.textAlign = "center";
            // context.font = this.fontSize * 2 + "px " + this.fontFamily;
            $('#gamemenu').fadeIn();
            $('#maincontainer').removeClass('clear');
            if (this.game.score > this.game.winningScore) {
                submitScore(this.game.score);
                context.fillText(
                    "你赢了, 分数 : " + this.game.score,
                    this.game.width * 0.5,
                    this.game.height * 0.5
                );
            } else {
                submitScore(this.game.score);
                context.fillText(
                    "游戏结束, 分数 :" + this.game.score,
                    this.game.width * 0.5,
                    this.game.height * 0.5
                );
            }
            context.font = this.fontSize * 1 + "px " + this.fontFamily;
            context.fillText(
                "按 “空格键” 重新开始",
                this.game.width * 0.5 + 5,
                this.game.height * 0.5 + 88
            );
        }
        context.restore();
    }
}
window.addEventListener("load", function () {
    const canvas = document.getElementById("canvas1");
    const ctx = canvas.getContext("2d");
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    class Game {
        constructor(width, height) {
            this.width = width;
            this.height = height;
            this.groundMargin = 120;
            this.speed = 0;
            this.maxSpeed = 3;
            this.background = new BackGround(this);
            this.player = new Player(this);
            this.input = new InputHandler(this);
            this.ui = new UI(this);
            this.enemies = [];
            this.particles = [];
            this.collisions = [];
            this.floatingMessages = [];
            this.maxParticles = 50;
            this.enemyInterval = 1000; //新敌人加入画面的速度，可以调节敌人出现的速度
            this.enemyTimer = 0;
            this.debug = false;
            this.score = 0;
            this.fontColor = "black";
            this.time = 0;
            this.maxTime = 60000;
            this.gameOver = false;
            this.lives = 5;
            this.winningScore = 40;
            this.player.currentState = this.player.states[0];
            this.player.currentState.enter();
        }
        update(deltaTime) {
            this.time += deltaTime;
            if (this.time > this.maxTime) this.gameOver = true;
            this.background.update();
            this.player.update(this.input.keys, deltaTime);
            // 敌人的更新控制
            if (this.enemyTimer > this.enemyInterval) {
                this.addEnemy();
                this.enemyTimer = 0;
            } else {
                this.enemyTimer += deltaTime;
            }
            this.enemies.forEach((enemy) => {
                enemy.update(deltaTime);
            });
            // 处理消除敌人消息
            this.floatingMessages.forEach((message) => {
                message.update();
            });
            // 处理粒子效果
            this.particles.forEach((particle, index) => {
                particle.update();
            });
            if (this.particles.length > this.maxParticles) {
                this.particles.length = this.maxParticles;
            }
            //    处理碰撞动画效果
            this.collisions.forEach((collision, index) => {
                collision.update(deltaTime);
            });
            this.enemies = this.enemies.filter(
                (enemy) => !enemy.markedForDeletion
            );
            this.particles = this.particles.filter(
                (particle) => !particle.markedForDeletion
            );
            this.collisions = this.collisions.filter(
                (collision) => !collision.markedForDeletion
            );
            this.floatingMessages = this.floatingMessages.filter(
                (message) => !message.markedForDeletion
            );
            // console.log(
            //     this.enemies,
            //     this.particles,
            //     this.collisions,
            //     this.floatingMessages
            // );
        }
        draw(context) {
            this.background.draw(context);
            this.player.draw(context);
            this.enemies.forEach((enemy) => {
                enemy.draw(context);
            });
            this.particles.forEach((particle) => {
                particle.draw(context);
            });
            this.collisions.forEach((collision) => {
                collision.draw(context);
            });
            this.floatingMessages.forEach((message) => {
                message.draw(context);
            });
            this.ui.draw(context);
        }
        addEnemy() {
            if (this.speed > 0 && Math.random() < 0.5)
                this.enemies.push(new GroundEnemy(this));
            else if (this.speed > 0) this.enemies.push(new ClimbingEnemy(this));
            this.enemies.push(new FlyingEnemy(this));
        }
    }
    let game = new Game(canvas.width, canvas.height);
    let lastTime = 0;
    function animate(timeStamp) {
        const deltaTime = timeStamp - lastTime;
        lastTime = timeStamp;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        game.update(deltaTime);
        game.draw(ctx);
        if (!game.gameOver) requestAnimationFrame(animate);
    }
    animate(0);

    window.addEventListener('keydown', e => {
        if(e.key == " " && game.gameOver) {
            $('#gameTitle').fadeOut();
            $('#gamemenu').fadeOut();
            $('#maincontainer').addClass('clear');
            game = new Game(canvas.width, canvas.height);
            game.input.bindEvent();
            animate(0);
        }
    });
    $('#btStart').on('click', function() {
        $('#gameTitle').fadeOut();
        $('#gamemenu').fadeOut();
        $('#maincontainer').addClass('clear');
        if(game.gameOver) {
            game = new Game(canvas.width, canvas.height);
            animate(0);
        }
        game.input.bindEvent();
    });
    window.game = game;
});