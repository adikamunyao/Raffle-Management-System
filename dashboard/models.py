from django.db import models


class LandingPageContent(models.Model):
	site_badge = models.CharField(max_length=120, default="Youth Day 2026 • Worship · Grow · Become")
	hero_title = models.CharField(max_length=180, default="Youth Day 2026 Raffle Draw")
	hero_tagline = models.CharField(max_length=160, default="WHERE EVERY SOUL MATTERS")
	hero_description = models.TextField(
		default=(
			"Join us as the youth of KAG Clayworks lead the entire Youth Day Sunday service. "
			"By purchasing a raffle ticket, you support youth ministry programs while standing "
			"a chance to win exciting prizes."
		)
	)

	primary_cta_text = models.CharField(max_length=80, default="Get Your Ticket")
	secondary_cta_text = models.CharField(max_length=80, default="Payment Instructions")
	hero_callout = models.CharField(
		max_length=140,
		default="Limited ticket numbers available. Secure your preferred lucky number before it's taken.",
	)

	ticket_price_note = models.CharField(max_length=120, default="KSh 500 per ticket")
	ticket_goal_note = models.CharField(
		max_length=180,
		default="Every ticket helps fund youth ministry activities, discipleship, outreach, and Youth Day initiatives.",
	)

	prize_section_title = models.CharField(max_length=140, default="15+ Winners Will Be Selected")
	prize_section_note = models.CharField(
		max_length=180,
		default="The more tickets we sell, the more prizes we add - so spread the word!",
	)

	grand_prize_label = models.CharField(max_length=80, default="Grand Prize")
	grand_prize_name = models.CharField(max_length=120, default="Smart TV")
	grand_prize_description = models.CharField(max_length=140, default="The big one - light up movie nights")
	grand_prize_icon = models.CharField(max_length=10, default="📺")
	grand_prize_image_url = models.URLField(blank=True, default="")

	second_prize_label = models.CharField(max_length=80, default="Second Prize")
	second_prize_name = models.CharField(max_length=120, default="2-Burner Gas Cooker")
	second_prize_description = models.CharField(max_length=140, default="Cook up something delicious")
	second_prize_icon = models.CharField(max_length=10, default="🔥")
	second_prize_image_url = models.URLField(blank=True, default="")

	third_prize_label = models.CharField(max_length=80, default="Third Prize")
	third_prize_name = models.CharField(max_length=120, default="Mobile Phone")
	third_prize_description = models.CharField(max_length=140, default="Stay connected in style")
	third_prize_icon = models.CharField(max_length=10, default="📱")
	third_prize_image_url = models.URLField(blank=True, default="")

	worship_title = models.CharField(max_length=60, default="Worship")
	worship_description = models.CharField(
		max_length=160,
		default="Strengthening praise and prayer in every youth gathering.",
	)
	grow_title = models.CharField(max_length=60, default="Grow")
	grow_description = models.CharField(
		max_length=160,
		default="Supporting growth in faith, leadership, and community service.",
	)
	become_title = models.CharField(max_length=60, default="Become")
	become_description = models.CharField(
		max_length=160,
		default="Helping young people become confident, compassionate leaders.",
	)

	support_title = models.CharField(max_length=120, default="Need Assistance?")
	support_description = models.TextField(
		default=(
			"If you experience any difficulties with payment, registration, ticket selection, "
			"or downloading your ticket, please contact the Youth Secretariat."
		)
	)
	support_phone = models.CharField(max_length=30, default="+254 715 550 805")

	faq_payment_answer = models.TextField(
		default=(
			"Pay KSh 500 via CoopBank to the official details on the payment instructions page, "
			"then submit your confirmation SMS when registering."
		)
	)
	faq_draw_answer = models.TextField(
		default=(
			"The draw takes place during the Youth Day Sunday service. Winners will be selected live "
			"and announced to the congregation."
		)
	)
	faq_more_tickets_answer = models.TextField(
		default="Yes. Each additional ticket increases your chance of winning and your support for the youth ministry.")
	faq_proceeds_answer = models.TextField(
		default=(
			"All proceeds go directly toward KAG Clayworks Youth Ministry programs - discipleship materials, "
			"outreach events, camps, and Royal Rangers activities."
		)
	)

	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Landing Page Content"
		verbose_name_plural = "Landing Page Content"

	def __str__(self):
		return self.hero_title
