def append_to_csv(wos_id, cited_wos_ids, field):
    """Populates csv with lead author of paper with wos_id provided
    NOTE:WOS:000246020100009 is the one we're using for now"""
    list_of_citation_wos_ids = cited_wos_ids
    citations = [get_info(paper) for paper in list_of_citation_wos_ids]
    c = csv.writer(open("{}_papers.csv".format(field), "a"))
    line = []
    db.connect()
    sql = """SELECT first_name,last_name,email_addr,title,abstract,pubyear
    FROM publications JOIN contributors
    ON contributors.wos_id=publications.wos_id
    JOIN abstracts ON abstracts.wos_id=contributors.wos_id
    WHERE contributors.wos_id='{}' AND position=2""".format(wos_id)
    # Position=2 because we are looking for a specific paper and
    # targeting author 2
    cursor = db.query(sql)
    res = cursor.fetchone()
    line.extend(list(res))
    line.append("Sample Amazon Gift Code")
    line.extend(citations)
    c.writerow(line)
