from flask import Blueprint, redirect, render_template, request, url_for

from business.services.affiliation_service import AffiliationService
from presentation.controllers.auth_controller import login_required, role_required


affiliation_bp = Blueprint("affiliation", __name__)
affiliation_service = AffiliationService()


@affiliation_bp.route("/")
@login_required
@role_required("admin", "auxiliar")
def index():
    affiliations = affiliation_service.list_affiliations()
    return render_template("afiliaciones/index.html", affiliations=affiliations)


@affiliation_bp.route("/<int:affiliation_id>/<action>", methods=["POST"])
@login_required
@role_required("admin", "auxiliar")
def change_state(affiliation_id, action):
    affiliation_service.change_state(
        affiliation_id,
        action,
        request.form.get("motivo_modificacion")
    )
    return redirect(url_for("affiliation.index"))