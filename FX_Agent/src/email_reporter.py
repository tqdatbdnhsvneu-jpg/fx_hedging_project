import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from jinja2 import Environment, FileSystemLoader

class EmailReporter:
    """Distributes the HTML C-Level Report Interface."""

    def __init__(self):
        self.template_dir = "templates"
        self.sender_email = "tqdat.bdn.hsv.neu@gmail.com"
        self.receiver_email = "tqdat.bdn.hsv.neu@gmail.com"
        self.password = os.getenv("EMAIL_PASSWORD")

    def _render_html(self, current_rate, prophet_signal, ai_insights, ai_feature_suggestions) -> str:
        env = Environment(loader=FileSystemLoader(self.template_dir))
        template = env.get_template("email_template.html")
        return template.render(
            current_rate=current_rate,
            prophet_signal=prophet_signal,
            ai_insights=ai_insights,
            ai_feature_suggestions=ai_feature_suggestions
        )

    def send_email(self, current_rate, prophet_signal, ai_dict, chart_path="forecast_chart.png"):
        msg = MIMEMultipart('related')
        msg['Subject'] = 'Daily FX_Agent Executive Briefing'
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email

        ai_insights = ai_dict.get("actionable_insights", [])
        ai_feature_suggestions = ai_dict.get("feature_engineering_suggestions", [])

        # Attach HTML
        html_content = self._render_html(current_rate, prophet_signal, ai_insights, ai_feature_suggestions)
        msg.attach(MIMEText(html_content, 'html'))

        # Embed Image explicitly tracking CID target identifier
        if os.path.exists(chart_path):
            with open(chart_path, 'rb') as img:
                mime_img = MIMEImage(img.read())
                mime_img.add_header('Content-ID', '<forecast_chart>')
                msg.attach(mime_img)

        # Broadcast Sequence
        if not self.password:
            print("[Warning] EMAIL_PASSWORD missing. Skipping the SMTP send sequence.")
            return

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.sender_email, self.password)
                server.send_message(msg)
        except smtplib.SMTPAuthenticationError:
            print("[CRITICAL] SMTP Authentication Failed. Check EMAIL_PASSWORD.")
        except Exception as e:
            print(f"[ERROR] Email dispatch failed completely: {str(e)}")
