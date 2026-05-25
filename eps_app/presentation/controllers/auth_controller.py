from functools import wraps

from flask import Blueprint, redirect, render_template, request, session, url_for

from business.services.auth_service import AuthService


auth_bp = Blueprint("auth", __name__)
auth_service = AuthService()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped


def role_required(*allowed_roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if session.get("rol") not in allowed_roles:
                return redirect(url_for("auth.dashboard"))
            return view(*args, **kwargs)

        return wrapped

    return decorator


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        user = auth_service.login(request.form["username"], request.form["password"])
        if user:
            session["user_id"] = user.id
            session["username"] = user.username
            session["rol"] = user.rol
            return redirect(url_for("auth.dashboard"))
        error = "Credenciales invalidas"
    return render_template("auth/login.html", error=error)


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@auth_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("auth/dashboard.html")