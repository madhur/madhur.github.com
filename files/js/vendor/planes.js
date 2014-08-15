var doodle = (function()
{
    Function.prototype.bind = Function.prototype.bind || function(u)
    {
        var v = this;
        return function()
        {
            return v.apply(u, arguments)
        }
    };
    var g = false;
    var a = function(u)
    {
        g && console && console.log && console.log(u)
    };
    var n = document.documentElement;
    var h = window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || function(u)
    {
        setTimeout(u, 17)
    };
    var m = Math.PI / 2,
        r = {};
    var b = function(u)
    {
        this.canvas = u;
        this.ctx = u.getContext("2d");
        this.objects = [];
        this.restart_timeout = 1000;
        this.paused = false;
        this.destroyed = false;
        return this
    };
    var e = 0,
        f, o = (new Date) * 1 - 1;
    var t = 50;
    var i = function()
    {
        var u = 1000 / ((f = new Date) - o);
        e += (u - e) / t;
        o = f
    };
    b.prototype.frame = function()
    {
        if (this.destroyed)
        {
            return
        }
        this.ctx.clearRect(0, 0, this.ctx.canvas.width, this.ctx.canvas.height);
        for (var v in this.objects)
        {
            if (this.objects[v].destroyed == true)
            {
                this.objects.splice(v, 1)
            }
            else
            {
                this.objects[v].tick(this.ctx)
            }
        }
        if (this.objects.length == 0)
        {
            var u = this;
            setTimeout(function()
            {
                a("restarting in " + u.restart_timeout);
                u.setup();
                u.frame()
            }, this.restart_timeout)
        }
        else
        {
            if (!this.paused)
            {
                h(this.frame.bind(this))
            }
        }
    };
    b.prototype.setup = function()
    {
        this.objects.push(d(this))
    };
    b.prototype.destroy = function()
    {
        this.destroyed = true;
        this.objects = []
    };
    var j = function(u, v)
    {
        this.x = u;
        this.y = v;
        this.planes = []
    };
    j.prototype.addPlane = function(w, u, x)
    {
        var z = this.x + w,
            y = this.y + u;
        var v = new c(r.jet_img, z, y, x, w, u);
        this.planes.push(v);
        return v
    };
    j.prototype.travelTo = function(u, B, w)
    {
        var A;
        for (var z in this.planes)
        {
            A = this.planes[z];
            A.travelTo(A.formation_x + u, A.formation_y + B, w)
        }
    };
    j.prototype.tick = function(u)
    {
        for (var v in this.planes)
        {
            if (this.planes[v].destroyed)
            {
                a("deleting plane " + v);
                this.planes.splice(v, 1)
            }
            else
            {
                this.planes[v].tick(u)
            }
        }
        if (this.planes.length == 0)
        {
            this.destroy()
        }
    };
    j.prototype.destroy = function()
    {
        this.destroyed = true
    };
    var d = function(w)
    {
        var z = Math.random() > 0.5 ? true : false;
        var u = z ? w.ctx.canvas.height : 10 + (w.ctx.canvas.height - 10) * Math.random();
        var v = z ? (w.ctx.canvas.width / 2 - 10) * Math.random() : 10;
        a("starting from:" + v + " ," + u);
        var A = new j(v, u);
        A.addPlane(0, 0, "255, 153, 51");
        A.addPlane(50, -50, "222, 222, 222");
        A.addPlane(100, 0, "0, 128, 0");
        var x = w.ctx.canvas.height - u;
        var y = w.ctx.canvas.width - v;
        A.travelTo(y, x, 3 + 3 * Math.random());
        return A
    };
    var c = function(y, x, v, z, w, u)
    {
        this.img = y;
        this.x = x;
        this.y = v;
        this.formation_x = w;
        this.formation_y = u;
        this.smoke_particles_list = [];
        this.smoke_rgb = z;
        this.destroy_plane = false;
        this.pather = new k();
        return this
    };
    c.prototype.draw = function(u)
    {
        u.save();
        var w = Math.atan(this.pather.slope) + m;
        u.translate(this.x, this.y);
        u.rotate(w);
        u.drawImage(this.img, 0, 0);
        u.restore();
        for (var v in this.smoke_particles_list)
        {
            if (this.smoke_particles_list[v].destroyed == true)
            {
                this.smoke_particles_list.splice(v, 1)
            }
            else
            {
                this.smoke_particles_list[v].draw(u)
            }
        }
    };
    c.prototype.travelTo = function(x, w, u)
    {
        this.pather.createPath(this.x, this.y, x, w, u)
    };
    c.prototype.tick = function(u)
    {
        this.pather.move();
        var A = Math.atan(this.pather.slope) + m;
        var y = -this.formation_x + this.formation_x * Math.cos(A) - this.formation_y * Math.sin(A);
        var x = -this.formation_y + this.formation_x * Math.sin(A) + this.formation_y * Math.cos(A);
        this.x = this.pather.x + y;
        this.y = this.pather.y + x;
        if (this.smoke_particles_list.length < 100 && !this.destroy_plane)
        {
            var B = (11 + 2 * Math.random()) * Math.cos(A) - (29 + 4 * Math.random()) * Math.sin(A);
            var z = (11 + 2 * Math.random()) * Math.sin(A) + (29 + 4 * Math.random()) * Math.cos(A);
            var v = new l(this.x + B, this.y + z, this.smoke_rgb);
            this.smoke_particles_list.push(v)
        }
        this.draw(u);
        var w = 50;
        if (this.x > u.canvas.width + w || this.y > u.canvas.height + w || this.x < 0 - w || this.y < 0 - w)
        {
            this.destroy_plane = true
        }
        else
        {
            this.destroy_plane = false
        } if (this.destroy_plane && this.smoke_particles_list.length == 0)
        {
            this.destroy()
        }
    };
    c.prototype.destroy = function()
    {
        this.destroyed = true
    };
    var k = function()
    {
        this.speed = 2.5;
        this.slope = null;
        this.x = 0;
        this.y = 0;
        this.delta_x = 0;
        this.delta_y = 0
    };
    k.prototype.createPath = function(x, z, w, y, u)
    {
        this.x = x;
        this.y = z;
        this.delta_x = w - x;
        this.delta_y = y - z;
        this.slope = this.delta_y / this.delta_x;
        this.speed = u
    };
    k.prototype.setSpeed = function(u)
    {
        this.speed = u
    };
    k.prototype.move = function()
    {
        this.x = this.x + Math.cos(Math.atan(this.slope)) * this.speed;
        this.y = this.y + Math.sin(Math.atan(this.slope)) * this.speed
    };
    var l = function(w, u, v)
    {
        this.x = w;
        this.y = u;
        this.opacity = 0.5;
        this.radius = 2 + Math.random();
        this.rgb = v
    };
    l.prototype.draw = function(u)
    {
        u.save();
        u.beginPath();
        u.fillStyle = "rgba(" + this.rgb + "," + this.opacity + ")";
        u.shadowColor = "rgba(" + this.rgb + ",1)";
        u.arc(this.x, this.y, this.radius, 0, Math.PI * 2, true);
        u.fill();
        this.radius = this.radius + 0.05;
        this.opacity = this.opacity - 0.005;
        if (this.opacity <= 0)
        {
            this.destroyed = true
        }
        u.restore()
    };
    var q;
    var p = function(w)
    {
        var v = document.createElement("canvas");
        v.id = "canvas_doodle";
        v.height = window.innerHeight || n.clientHeight;
        v.width = window.innerWidth || n.clientWidth;
        var u = v.style;
        u.position = "fixed";
        u.top = 0;
        u.left = 0;
        u.zIndex = 1138;
        u.pointerEvents = "none";
        document.body.appendChild(v);
        q = new b(v);
        r.jet_img = new Image();
        r.jet_img.src = w;
        r.jet_img.onload = function()
        {
            q.setup();
            h(q.frame.bind(q))
        }
    };
    var s = function()
    {
        q.destroy();
        setTimeout(function()
        {
            document.body.removeChild(document.getElementById("canvas_doodle"))
        }, 50);
        delete q
    };
    return {
        init: p,
        destroy: s
    }
})();