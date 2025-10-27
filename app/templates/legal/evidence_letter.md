# 存證信函（附件版模板）
**編號：** {{ doc_no }}
**日期：** {{ date }}
**寄件人：** {{ sender }}
**收件人：** {{ recipient }}

## 正文
{{ body }}

## 附件
{% for item in attachments %}
- {{ item }}
{% endfor %}
