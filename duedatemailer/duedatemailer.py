from datetime import datetime, timedelta
from trac.core import *
from trac.ticket import TicketSystem, Ticket
from trac.admin.api import IAdminCommandProvider
from trac.util.text import printout
from trac.util.datefmt import parse_date, to_timestamp, utc

class DueDateMailer(Component):
	implements(IAdminCommandProvider)

	soft_diff_threshold = timedelta(4)
	diff_threshold = timedelta(4)

	def get_admin_commands(self):
		yield ('ticket checkdates', '',
			'Check the due dates on tickets, send notifications when they are close',
			None, self._do_checkdates)

	def _do_checkdates(self):
		ts = TicketSystem(self.env)
		now = datetime.now(utc)
		hard_mail = []
		soft_mail = []
		with self.env.db_query as db:
			cursor = db.cursor()
			cursor.execute("SELECT id FROM ticket WHERE status != 'closed'")
			for row in cursor:
				ticket_id = row[0]
				t = Ticket(self.env, ticket_id, db)
				t['id'] = ticket_id
				if t['due_date']:
					due_diff = parse_date(t['due_date']) - now
					if due_diff <= self.diff_threshold:
						hard_mail.append(t)
				elif t['soft_due_date']:
					soft_due_diff = parse_date(t['soft_due_date']) - now
					if soft_due_diff <= self.soft_diff_threshold:
						soft_mail.append(t)

		if len(hard_mail) == 0 and len(soft_mail) == 0:
			return

		mail_body = "This is your friendly Ticket Due Date Mailer for today.\n\n"

		hard_mail=sorted(hard_mail, key=lambda ticket: ticket['due_date'])
		soft_mail=sorted(soft_mail, key=lambda ticket: ticket['soft_due_date'])

		if len(hard_mail) != 0:
			mail_body += "The following tickets are nearing their HARD DEADLINE:\n"
			mail_body +=         "    id  due_date       component  summary\n"
			for ticket in hard_mail:
				mail_body += "  % 4d  %s  % 12s  %s\n" % (ticket['id'], ticket['due_date'], ticket['component'], ticket['summary'])
			mail_body += "\n"

		if len(soft_mail) != 0:
			mail_body += "The following tickets are nearing their SOFT DEADLINE:\n"
			mail_body +=         "    id  soft_due_date  component  summary\n"
			for ticket in soft_mail:
				mail_body += "  % 4d  %s  % 12s  %s\n" % (ticket['id'], ticket['soft_due_date'], ticket['component'], ticket['summary'])
			mail_body += "\n"

		mail_body += "See you next time!\n"
		mail_body += "Trac Assistent"
		print mail_body,
