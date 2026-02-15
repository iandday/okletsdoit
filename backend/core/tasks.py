import io

from celery import shared_task
from django.core.management import call_command


@shared_task
def run_management_command(command_name, *args, **kwargs):
    """
    A Celery task to run a Django management command.
    """
    out = io.StringIO()
    err = io.StringIO()
    try:
        call_command(command_name, *args, stdout=out, stderr=err, **kwargs)
        result = out.getvalue()
        error = err.getvalue()
        if error:
            raise Exception(f"Error running command {command_name}: {error}")
        return result
    except Exception as e:
        raise Exception(f"Exception occurred while running command {command_name}: {str(e)}")
    finally:
        out.close()
        err.close()


@shared_task
def send_update_email():
    """
    Celery task to send wedding planning update email to users with email notifications enabled.
    """
    out = io.StringIO()
    err = io.StringIO()
    try:
        call_command("send_update_email", stdout=out, stderr=err)
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
