from django.contrib import admin

from dashboard.models import LandingPageContent


@admin.register(LandingPageContent)
class LandingPageContentAdmin(admin.ModelAdmin):
	list_display = ("hero_title", "site_badge", "updated_at")
	fieldsets = (
		("Hero", {
			"fields": (
				"site_badge",
				"hero_title",
				"hero_tagline",
				"hero_description",
				"hero_callout",
				"primary_cta_text",
				"secondary_cta_text",
			)
		}),
		("Tickets", {
			"fields": (
				"ticket_price_note",
				"ticket_goal_note",
			)
		}),
		("Prizes", {
			"fields": (
				"prize_section_title",
				"prize_section_note",
				("grand_prize_label", "grand_prize_name"),
				"grand_prize_description",
				"grand_prize_icon",
				"grand_prize_image_url",
				("second_prize_label", "second_prize_name"),
				"second_prize_description",
				"second_prize_icon",
				"second_prize_image_url",
				("third_prize_label", "third_prize_name"),
				"third_prize_description",
				"third_prize_icon",
				"third_prize_image_url",
			)
		}),
		("Worship, Grow, Become", {
			"fields": (
				("worship_title", "worship_description"),
				("grow_title", "grow_description"),
				("become_title", "become_description"),
			)
		}),
		("Support & FAQ", {
			"fields": (
				"support_title",
				"support_description",
				"support_phone",
				"faq_payment_answer",
				"faq_draw_answer",
				"faq_more_tickets_answer",
				"faq_proceeds_answer",
			)
		}),
	)
