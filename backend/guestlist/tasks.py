from celery import shared_task
from django.core.management import call_command
import io
from core.models import WeddingSettings


@shared_task
def generate_missing_qr_codes():
    """
    Celery task to generate QR codes for guest groups that don't have one.
    """
    out = io.StringIO()
    err = io.StringIO()
    try:
        call_command("generate_rsvp_qr", stdout=out, stderr=err)
        result = out.getvalue()
        error = err.getvalue()
        if error:
            return {"success": False, "error": error, "output": result}
        return {"success": True, "output": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        out.close()
        err.close()


@shared_task
def regenerate_all_qr_codes():
    """
    Celery task to regenerate ALL QR codes for guest groups.
    """
    out = io.StringIO()
    err = io.StringIO()
    try:
        call_command("generate_rsvp_qr", "--regenerate", stdout=out, stderr=err)
        result = out.getvalue()
        error = err.getvalue()
        if error:
            return {"success": False, "error": error, "output": result}
        w_settings = WeddingSettings.objects.first()
        if w_settings:
            w_settings.save()  # Update timestamp to trigger qr code regeneration
        return {"success": True, "output": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        out.close()
        err.close()
