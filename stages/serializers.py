from rest_framework import serializers

from players.models import Player
from stages.models import Phase, GamePlay, Stage, GamePlayStage


class PlayStageSerializer(serializers.Serializer):
    phase = serializers.PrimaryKeyRelatedField(queryset=Phase.objects.all())
    slot1_skill = serializers.BooleanField()
    slot2_skill = serializers.BooleanField()
    slot3_skill = serializers.BooleanField()
    slot4_skill = serializers.BooleanField()
    slot5_skill = serializers.BooleanField()
    boost = serializers.BooleanField(allow_null=True)


class PhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phase
        exclude = ["modified_at", "created_at"]


class GamePlayStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamePlayStage
        exclude = ["modified_at", "created_at"]


class GamePlaySerializer(serializers.ModelSerializer):
    phase = PhaseSerializer()
    next_phase_id = serializers.SerializerMethodField()
    game_play_stage = GamePlayStageSerializer()

    def get_next_phase_id(self, obj):
        next_phase = Phase.objects.filter(stage=obj.phase.stage,
                                          phase_no=obj.phase.phase_no + 1)
        if next_phase.exists():
            return next_phase.first().id
        return None

    class Meta:
        model = GamePlay
        exclude = ["modified_at"]


class PhaseOverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phase
        fields = ["id", "phase_no"]


class StageSerializer(serializers.ModelSerializer):
    phases = PhaseOverviewSerializer(source='phase_stage', many=True)
    is_cleared = serializers.SerializerMethodField()

    def get_is_cleared(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            player = Player.objects.get(user=user)
            return GamePlayStage.objects.filter(stage=obj, player=player, is_win=True).exists()
        return False

    class Meta:
        model = Stage
        exclude = ["modified_at", "created_at"]
