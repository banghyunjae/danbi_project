from django.db import models


class Team(models.Model):  # Team 모델 단비, 다래, 블라블라, 철로, 땅이, 해태, 수피
    name = models.CharField(max_length=50, unique=True)


class Task(models.Model):  # Task 모델 팀명, 업무명, 업무내용, 완료여부, 완료일자, 생성일자, 수정일자
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=30)
    content = models.TextField()
    is_complete = models.BooleanField(default=False)
    completed_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class SubTask(models.Model):  # SubTask 모델 팀명, 업무명, 완료여부, 완료일자, 생성일자, 수정일자
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_subtasks")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_subtasks")
    is_complete = models.BooleanField(default=False)
    completed_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


# User 부분은 앱기능을 따로 만들어서 로그인 회원가입을 구현
# JWT 토큰을 이용해서 로그인 회원가입 구현 예정
# fommater를 이용해서 black 사용

# 시나리오
"""
단비교육에 김윙크 사원이 단비팀으로 입사를 했습니다.
김윙크 사원이 업무를 할당받았습니다. 혼자서는 업무를 처리 할 수 없어 다른 팀들의 도움이 필요합니다.
단비교육에는 단비, 다래, 블라블라, 철로, 땅이, 해태, 수피 7개의 팀이 있습니다.
할당받은 업무(Task)를 진행하기 위해서 김윙크 사원은 협업이 필요한 팀에게 업무를 요청하려고 합니다.
이를 위해 김윙크 사원은 업무(Task)를 생성해야 합니다. 업무(Task)생성 시, 협업이 필요한 팀을 하위업무(SubTask)로 설정하면 해당 팀들에게
업무를 요청할 수 있게됩니다.

이번 과제에서는 위와같은 요청사항을 처리할 수 있는 시스템을 개발하려고 합니다.
업무(Task) 생성시에는 아래와 같은 조건을 만족해야 합니다.
업무 생성 시, 한 개 이상의 팀을 설정해야합니다.(1)

단, 업무(Task)를 생성하는 팀이 반드시 하위업무(SubTask)에 포함되지는 않습니다.(2)
ex) 단비 Team이 업무(Task) 생성 시 하위 업무로 단비, 다래, 철로 Team을 설정할 수 있습니다. 단, 단비팀이 업무를 진행하지 않아도
될 경우에는 꼭 하위업무에 단비팀이 들어가지 않아도 됩니다.

단, 정해진 7개의 팀 이외에는 다른 팀에 하위업무(SubTask)를 부여할 수 없습니다.(3)
단, 업무(Task)를 수정할 경우 하위업무(SubTask)의 팀들도 수정 가능합니다.(4) 
단, 완료된 하위업무(SubTask)에 대해서는 삭제처리는 불가능합니다.(5)
ex) 단비 Team이 업무(Task) 생성 시 하위 업무(SubTask)단비, 다래, 철로 Team을 설정 후 하위업무팀을 단비만 하도록 하거나 단비, 다
래, 수피 팀으로 유동적으로 변경가능합니다. 변경시 완료된 하위업무(SubTask) 있다면 무시합니다.

조건
업무(Task) 조회 시 하위업무(SubTask)에 본인 팀이 포함되어 있다면 업무목록에서 함께 조회가 가능해야합니다.(6)
업무(Task) 조회 시 하위업무(SubTask)의 업무 처리여부를 확인할 수 있어야 합니다.(7)
업무(Task)는 작성자 이외에 수정이 불가합니다.(8)
업무(Task)에 할당된 하위업무(SubTask)의 팀(Team)은 수정, 변경 가능해야 합니다. 단 해당 하위업무(SubTask)가 완료되었다면 삭제되지
않아야 합니다.(9)
업무(Task)의 모든 하위업무(SubTask)가 완료되면 해당 상위업무(Task)는 자동으로 완료처리가 되어야합니다.(10)
하위업무(SubTask) 완료 처리는 소속된 팀만 처리 가능합니다.(11)

# Task
- id ( )
- create_user ()
- team ( )
- title ( )
- content ( )
- is_complete ( , default=False)
- completed_date ( )
- created_at ( )
- modified_at ( )

# SubTask
- id ( )
- team ( )
- is_complete ( , default=False)
- completed_date ( )
- created_at ( )
- modified_at ( )

# USER(abstract)
- id ( )
- username ( )
- pw ( )
- team ()
"""

# Team 모델 단비, 다래, 블라블라, 철로, 땅이, 해태, 수피 (o)
# Task 모델 팀명, 업무명, 업무내용, 완료여부, 완료일자, 생성일자, 수정일자 (o)
# SubTask 모델 팀명, 업무명, 완료여부, 완료일자, 생성일자, 수정일자 (o)
# (1) Task 생성시 한개 이상의 팀을 설정해야함 ()
# (2) Task 생성하는 팀이 반드시 하위업무에 포함되지 않아도 됨 ()
# (3) 정해진 7개의 팀 이외에는 다른 팀에 하위업무를 부여할 수 없음 ()
# (4) Task 수정시 하위업무의 팀들도 수정 가능 ()
# (5) 완료된 하위업무에 대해서는 삭제처리 불가능 ()
# (6) Task 조회시 하위업무에 본인 팀이 포함되어 있다면 업무목록에서 함께 조회가 가능해야함 ()
# (7) Task 조회시 하위업무의 업무 처리여부를 확인할 수 있어야함 ()
# (8) Task는 작성자 이외에 수정이 불가능 ()
# (9) Task에 할당된 하위업무의 팀은 수정, 변경 가능해야함. 단 해당 하위업무가 완료되었다면 삭제되지 않아야함 ()
# (10) Task의 모든 하위업무가 완료되면 해당 상위업무는 자동으로 완료처리가 되어야함 ()
# (11) 하위업무 완료처리는 소속된 팀만 처리 가능 ()
