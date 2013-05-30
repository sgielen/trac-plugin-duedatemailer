trac-plugin-duedatemailer
=========================

This plugin implements sending notification e-mails when a plugin is nearing
its hard or soft due date.

At the moment, it adds a "ticket checkdates" command to trac-admin which
outputs a nice list of tickets that should be checked soon.  If there is no
such ticket, the command outputs nothing. This allows its use in cron setups
where cron automatically sends the user an e-mail when a command outputs
something. For example, add the following line to crontab to do a tickets check
every night at 3:00:

    0 3 * * * /usr/local/bin/trac-admin /var/www/private.sjorsgielen.nl/trac ticket checkdates

Eventually, the plugin should be able to send e-mails to the relevant trac
users itself (by ticket metadata or by component). Also, it should be
configurable to use any field instead of the hard-coded `due_date` and
`soft_due_date` fields. It should maybe also send HTML e-mail so the lines can
be hyperlinks to the tickets (or a URL could be inserted on the next line).
