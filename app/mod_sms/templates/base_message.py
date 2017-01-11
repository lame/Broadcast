def base_message(user, message, user_group=None):
    resp = '''{body}\n
      from: {fname} {lname}
    '''.format(body=message.body, fname=user.fname, lname=lname)
    return resp
