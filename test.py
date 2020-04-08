import pandas as pd
a = {"CPU Usage": [["%CPU", "%MEM", "PID", "PPID", "USER", "STAT", "COMMAND"], ["2.1", "0.5", "1", "0", "root", "Ss", "/usr/lib/systemd/systemd --switched-root --system --deserialize 22 "], ["0.5", "0.8", "3381", "3337", "root", "Ss", "sshd: ec2-user [priv] "], ["0.1", "3.4", "1929", "1", "root", "Ss", "/usr/lib/systemd/systemd-journald "], ["0.1", "0.0", "8", "2", "root", "I", "[rcu_sched]"], ["0.0", "1.2", "3220", "1", "root", "Ssl", "/usr/bin/amazon-ssm-agent "]], "Memory Available": [["", "total", "used", "free", "shared", "buff/cache", "available"], ["Mem:", "983", "57", "738", "0", "187", "792 "], ["Swap:", "0", "0", "0"]], "OS & Kernel Info": [["Linux ip-172-31-7-84.ap-south-1.compute.internal 4.14.171-136.231.amzn2.x86_64 #1 SMP Thu Feb 27 20:22:48 UTC 2020 x86_64x86_64 x86_64 GNU/Linux "]], "Uptime": [["03:06:46 up 1 min, 0 users, load average: 0.10, 0.05, 0.02 "]], "Mount Disk usage": [["/dev/xvda1 xfs 8.0G 1.5G 6.6G 19% / "]]}


for resp_iter in a:
    initer = 0
    for li in a[resp_iter]:
        for each_value in li:
            if initer == 0:
                 print(each_value)
            else:
                #print("value- {}".format(each_value))
                pass
initer+= 1



'''
<h2>Enter the Ip/Hostname : </h2>
<form action="/send" method="post">
<div class="form-group">
  <input type="text" name="ip">
</div>
<input class="btn btn-primary" type="submit" value="Submit">
</form>

'''


#{"CPU Usage": [["%CPU", "%MEM", "PID", "PPID", "USER", "STAT", "COMMAND"], ["2.1", "0.5", "1", "0", "root", "Ss", "/usr/lib/systemd/systemd --switched-root --system --deserialize 22 "], ["0.5", "0.8", "3381", "3337", "root", "Ss", "sshd: ec2-user [priv] "], ["0.1", "3.4", "1929", "1", "root", "Ss", "/usr/lib/systemd/systemd-journald "], ["0.1", "0.0", "8", "2", "root", "I", "[rcu_sched]"], ["0.0", "1.2", "3220", "1", "root", "Ssl", "/usr/bin/amazon-ssm-agent "]], "Memory Available": [["", "total", "used", "free", "shared", "buff/cache", "available"], ["Mem:", "983", "57", "738", "0", "187", "792 "], ["Swap:", "0", "0", "0"]], "OS & Kernel Info": [["Linux ip-172-31-7-84.ap-south-1.compute.internal 4.14.171-136.231.amzn2.x86_64 #1 SMP Thu Feb 27 20:22:48 UTC 2020 x86_64x86_64 x86_64 GNU/Linux "]], "Uptime": [["03:06:46 up 1 min, 0 users, load average: 0.10, 0.05, 0.02 "]], "Mount Disk usage": [["/dev/xvda1 xfs 8.0G 1.5G 6.6G 19% / "]]}
#
#

'''
{% for i in values %}
{% for len in len_list %}
  {% for j in range(len) %}
      <th>{{ values[i][0][j] }}</th>
      <td>{{ values[i] }}</td>
      {% endfor %}
  {% endfor %}
{% endfor %}
</tr>
'''


'''
{% for i,v in values.items() %}
<th> {{ i }} </th>
{% for val in v %}
<tr>
<td> {{ val }}</td>
</tr>
{% endfor %}
{% endfor %}
'''

'''
{% for i,v in values.items() %}
<tr>
<th> {{ i }} </th>
{% endfor %}
{% for val in v %}
</tr>
{% for i in range(0, len(results[a])) %}
<tr>
<td> {{ val }}</td>
</tr>
{% endfor %}
{% endfor %}
'''




'''
{% for resp_iter in values %}
{% set count = 1 %}
<table class="content-table">
<h3>{{ resp_iter }}</h3>
<tr>
{% for li in values[resp_iter] %}
    {% for val in li %}
        {% if count == 0 %}
            <th> {{ val }} </th>
        {% else %}
            <td> {{ val }} </td>
        {% endif %}
    {% endfor %}
    {% set count = count + 1 %}
</tr>

{% endfor %}
</table>
{% endfor %}



'''



'''
<table class="content-table">
  <tr>
  <th>Machine</th>
  <th>CPU %</th>
  <th>Memory %</th>

  {% for row in list %}



    <tr>
      {% for item in row %}
        {% if loop.index == 1 %}
        <form action="/send" method="post">
          <td><button btn style="border:none; border-bottom: 1px solid black;">{{ item }}</button></td>
          <input type="hidden" name="ip" value="{{ item }}" />
        </form>
        {% else %}
          {% if item > 75 %}
          <td class="over-limit"> {{item}} </td>
          {% elif item > 50 and  item < 75 %}
          <td class="average-limit"> {{item}} </td>
          {% else %}
          <td class="below-limit"> {{item}} </td>
          {% endif %}
        {% endif %}

      {% endfor %}

    </tr>
  {% endfor %}

  </tr>

</table>


'''




###csss
'''
* {
font-family: sans-serif; /* Change your font family */
}

.over-limit { background-color: #FF3333; }

.average-limit { background-color: #FFFF99; }

.below-limit { background-color: #80FF00; }

.content-table {
border-collapse: collapse;
margin: 25px 0;
margin-left:auto;
margin-right:auto;
font-size: 0.9em;
min-width: 400px;
border-radius: 10px 7px 3px 2px;
verflow: hidden;
box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
}

.content-table tr td:first-letter{
text-transform:capitalize;
}
.content-table thead tr {
background-color: #009879;
color: #ffffff;
text-align: center;
font-weight: bold;
}

.content-table th{
padding: 12px 15px;
text-transform: capitalize;
}
.content-table td {
padding: 12px 15px;
}

.content-table tbody tr {
border-bottom: 1px solid #dddddd;
}



.content-table tbody tr.active-row {
font-weight: bold;
color: #009879;
}
'''
