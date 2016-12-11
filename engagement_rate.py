import datetime, dateutil.parser
from collections import defaultdict
import logging

def GetOrderedCommentsByDate(comments):
	"""Returns a list containing the count of comments by date,
	sorted by date.

	Args:
		comments: The dict representing the comment.
	Returns:
		orderedCommentsCount: List of ints.
	"""
	comments_by_date = {}
	for comment in comments:
		if comment.get('postedDate'):
			comment_date = dateutil.parser.parse(comment.get('postedDate')).strftime('%m/%d/%Y')
			if comment_date in comments_by_date:
				comments_by_date[comment_date] += 1
			else:
				comments_by_date[comment_date] = 1
	dates = list(comments_by_date.iterkeys())
	dates.sort()
	orderedCommentsCount = [comments_by_date[date] for date in dates]
	return orderedCommentsCount

def ListAvg(arr):
	return sum(arr)/len(arr)

def CalculateEngagementTrend(comments):
	"""Calculates the engagement trend for the dict of comments passed.
	if n is the number of days ( sorted ) with comments, we compare the
	moving avg number of comments in the last 3 days (with comments) and
	compare it to the moving average for the previous set of dates.
	1 means Increased engagedment, -1 means reduced engagement
	and 0 means no change in engagement.

	Args:
		comments: The dict representing the comment.
	Returns:
		boolean: represents the engagement trend.
	"""
	orderedCommentsCount = GetOrderedCommentsByDate(comments)
	moving_avg = []
	set_count = 3
	dates_count = len(orderedCommentsCount)
	if dates_count <= 3:
		return 0

	for index in range(0, len(orderedCommentsCount)-3):
		moving_avg.append(ListAvg(orderedCommentsCount[index:index+3]))

	count_of_avgs = len(moving_avg)
	if moving_avg[count_of_avgs-1] > moving_avg[count_of_avgs-2]:
		return 1
	elif moving_avg[count_of_avgs-1] < moving_avg[count_of_avgs-2]:
		return -1
	else:
		return 0