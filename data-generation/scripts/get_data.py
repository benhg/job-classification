#!/usr/bin/env python3

import datetime
import pollster

api = pollster.Api()

# GET /tags
print()
print('GET /tags...')

tags = api.tags_get()

print('  Found %d tags' % len(tags))
print('  First tag: %s (%d charts)' % (tags[0].slug, tags[0].n_charts))

# GET /charts
print()
print('GET /charts...')

charts = api.charts_get(
    # String | Special string to index into the Array
    cursor=None,
    # String | Comma-separated list of tag slugs
    tags='2016-president',
    election_date=datetime.date(2016, 11, 8)  # Date | Date of an election
)

print('  Found %d charts; our results page has %d charts' %
      (charts.count, len(charts.items)))

# GET /charts/:slug
print()
print('GET /charts/:slug...')
chart_slug = charts.items[0].slug
print('  First chart has slug `%s`' % chart_slug)

chart = api.charts_slug_get(chart_slug)

print('  Found chart `%s`' % chart.slug)
print('  Tags: %s' % (','.join(chart.tags),))
print('  Question: %s' % chart.question.slug)
print('  Polls that answer Question: %d' % chart.question.n_polls)

# GET /polls, and pagination
print()
print('GET /polls...')
# Pick a question that has enough polls that we'll need to paginate
question_slug = next(
    c.question.slug for c in charts.items if c.question.n_polls > 30)

polls = api.polls_get(
    question=question_slug,
    sort='created_at'
)

print('  Found %d polls; our results page has %d polls and begins with %s' %
      (polls.count, len(polls.items), polls.items[0].slug))
print('  next_cursor is %s; using it in another GET request...' %
      polls.next_cursor)

polls2 = api.polls_get(
    question=question_slug,
    sort='created_at',
    cursor=polls.next_cursor
)

print('  Got another %d polls, such as %s' %
      (len(polls2.items), polls2.items[0].slug))

# GET /polls/:slug -- unnecessary here, since a Poll's data shows up in GET /polls
print()
print('GET /polls/:slug...')
poll_slug = polls.items[0].slug
print('  First poll has slug `%s`' % poll_slug)

poll = api.polls_slug_get(poll_slug)

print('  Found poll `%s`' % poll.slug)
print('  Poll conducted from: %s to: %s, entered into Pollster: %s' % tuple(
    t.isoformat() for t in [poll.start_date, poll.end_date, poll.created_at]))
print('  Questions: %d' % len(poll.poll_questions))
print('  First question name: %s' % poll.poll_questions[0].question.name)
print('  First question options: %s' % ', '.join(
    r.label for r in poll.poll_questions[0].question.responses))
print('  First question first sample subpopulation: %s' %
      poll.poll_questions[0].sample_subpopulations[0].name)


def simple_format_response(r):
    return '%s (%s): %0.1f' % (r.text, r.pollster_label, r.value)


print('  First question responses: %s' % '; '.join(simple_format_response(r)
                                                   for r in poll.poll_questions[0].sample_subpopulations[0].responses))

# GET /charts/:slug/pollster-trendlines.tsv
# returns a pandas.DataFrame
print()
print('GET /charts/:slug/pollster-trendlines.tsv... (slug: %s)' % chart_slug)

trendlines = api.charts_slug_pollster_trendlines_tsv_get(chart_slug)
print('  Found %d trendline points' % len(trendlines))

print('  The raw return value looks like this:')
print(repr(trendlines[0:5]))
print('...')

print('  Rearranged, it can look like this:')
by_date = trendlines.pivot(
    index='date', columns='label', values='value').sort_index(0, ascending=False)
print(repr(by_date[0:5]))
print('...')

# GET /charts/:slug/pollster-chart-poll-questions.tsv
print('')
print('GET /charts/:slug/pollster-chart-poll-questions.tsv... (%s)' % chart_slug)

chart_poll_questions = api.charts_slug_pollster_chart_poll_questions_tsv_get(
    chart_slug)

print('  Found %d poll questions plotted on chart:' %
      len(chart_poll_questions))
print(repr(chart_poll_questions[0:5]))
print('...')

# GET /questions
print()
print('GET /questions...')

questions = api.questions_get(
    # String | Special string to index into the Array
    cursor=None,
    # String | Comma-separated list of tag slugs (most Questions are not tagged)
    tags='2016-president',
    election_date=datetime.date(2016, 11, 8)  # Date | Date of an election
)

print('  Found %d questions; our results page has %d questions' %
      (questions.count, len(questions.items)))
print('  First Question: %s (%s)' %
      (questions.items[0].slug, questions.items[0].name))
print('  Responses Pollster tracks: %s' % ', '.join(
    map(lambda r: r.label, questions.items[0].responses)))

# GET /question/:slug/poll_responses_clean.tsv
print()
print('GET /question/:slug/poll_responses_clean.tsv... (for %s)' % question_slug)

responses_clean = api.questions_slug_poll_responses_clean_tsv_get(
    question_slug)

print('  Found %d responses to Question %s' %
      (len(responses_clean), question_slug))
print(repr(responses_clean[0:5]))
print('...')

# GET /question/:slug/poll_responses_raw.tsv
print()
print('GET /question/:slug/poll_responses_raw.tsv... (again, for %s)' %
      question_slug)

responses_raw = api.questions_slug_poll_responses_raw_tsv_get(question_slug)

print('  Found %d response data points to Question %s' %
      (len(responses_raw), question_slug))
print(repr(responses_raw[0:10]))
print('...')
