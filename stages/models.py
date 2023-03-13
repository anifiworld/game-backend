from django.db import models

from players.models import Player


def default_reward_dict():
    return {
        "items": [],
        "coin": 0,
        "gold": 0,
        "exp": 0
    }


def default_enemy_dict():
    return {
        "slot1": None,
        "slot2": None,
        "slot3": None,
        "slot4": None,
        "slot5": None,
    }


def default_hp_dict():
    return {
        "slot1": 0,
        "slot2": 0,
        "slot3": 0,
        "slot4": 0,
        "slot5": 0,
    }


def default_skill_cool_down_dict():
    return {
        "slot1": 0,
        "slot2": 0,
        "slot3": 0,
        "slot4": 0,
        "slot5": 0,
    }


def default_skill_cool_down_dict():
    return {
        "slot1": 0,
        "slot2": 0,
        "slot3": 0,
        "slot4": 0,
        "slot5": 0,
    }


def default_play_data_dict():
    return {
        'hero': {
            "slot1": None,
            "slot2": None,
            "slot3": None,
            "slot4": None,
            "slot5": None,
        },
        'has_next_phase': False,
        'game_sequence': []
    }


def default_monsters_dict():
    return []


class Stage(models.Model):
    name = models.CharField(max_length=255, unique=True)
    monsters = models.JSONField(default=default_monsters_dict)
    require_stage = models.ForeignKey("self", null=True, default=None, on_delete=models.RESTRICT,
                                      related_name="stage_require_stage")
    boost_cost = models.IntegerField(default=0)
    stamina_cost = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    reward = models.JSONField(default=None, null=True)

    def __str__(self) -> str:
        return self.name

    def gen_reward(self):
        phases = Phase.objects.filter(stage=self)
        result_reward = {
            "coin": 0,
            "gold": 0,
            "exp": 0,
            "items": []
        }
        items_obj = {}
        for phase in phases:
            if phase.reward is not None:
                result_reward["coin"] += phase.reward["coin"]
                result_reward["gold"] += phase.reward["gold"]
                result_reward["exp"] += phase.reward["exp"]
                for item in phase.reward["items"]:
                    if item["nft_id"] in items_obj:
                        items_obj[item["nft_id"]] += item["amount"]
                    else:
                        items_obj[item["nft_id"]] = item["amount"]
        for key, value in items_obj.items():
            result_reward["items"].append({
                "nft_id": key,
                "amount": value
            })
        self.reward = result_reward
        self.save()


class Phase(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name="phase_stage")
    phase_no = models.IntegerField()

    reward = models.JSONField(default=default_reward_dict)
    enemy = models.JSONField(default=default_enemy_dict)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['stage', 'phase_no'], name='unique_stage_phase_no')
        ]


class GamePlayStage(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name="game_play_stage")
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="game_play_stage_player")
    is_win = models.BooleanField(default=None, null=True)
    is_completed = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    is_boosted = models.BooleanField(default=False)
    current_game_play = models.ForeignKey('GamePlay', default=None, null=True, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class GamePlay(models.Model):
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE)
    game_play_stage = models.ForeignKey(GamePlayStage, on_delete=models.CASCADE,
                                        related_name="game_play_game_play_stage", default=None)
    play_data = models.JSONField(default=default_play_data_dict)
    start_hp = models.JSONField(default=default_hp_dict)
    result_hp = models.JSONField(default=default_hp_dict)
    skill_cool_down = models.JSONField(default=default_skill_cool_down_dict)
    is_win = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['game_play_stage', 'phase'], name='unique_game_play_stage_phase')
        ]
