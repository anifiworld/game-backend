from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.utils import timezone
from heroes.serializers import HeroUserSlotSerializer
from players.models import Player
from stages.models import GamePlay, Phase, GamePlayStage, Stage
from stages.serializers import PlayStageSerializer, GamePlaySerializer, PhaseSerializer, StageSerializer


class StageData(generics.RetrieveAPIView):
    serializer_class = StageSerializer
    permission_classes = [IsAuthenticated]
    queryset = Stage.objects.all()

    def get(self, request, *args, **kwargs):
        uncached_stage = self.get_queryset().filter(reward__isnull=True)
        for stage in uncached_stage:
            stage.gen_reward()
        return self.retrieve(request, *args, **kwargs)


class PhaseData(generics.RetrieveAPIView):
    serializer_class = PhaseSerializer
    permission_classes = [IsAuthenticated]
    queryset = Phase.objects.all()


class StageList(generics.ListAPIView):
    serializer_class = StageSerializer
    permission_classes = [IsAuthenticated]
    queryset = Stage.objects.all()

    def get(self, request, *args, **kwargs):
        uncached_stage = self.get_queryset().filter(reward__isnull=True)
        for stage in uncached_stage:
            stage.gen_reward()
        return self.list(request, *args, **kwargs)


class CancelStage(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        player = Player.objects.filter(user=self.request.user).first()
        if player is None:
            return Response({"error": "Player is not exists"}, status=status.HTTP_400_BAD_REQUEST)
        if player.game_play_stage is None or player.game_play_stage.is_completed:
            return Response({"error": "Not playing"}, status=status.HTTP_400_BAD_REQUEST)
        player.game_play_stage.is_win = False
        player.game_play_stage.is_completed = True
        player.game_play_stage.is_cancelled = True
        player.game_play_stage.save()
        player.game_play_stage = None
        player.save()
        return Response(status=status.HTTP_200_OK)


class PlayStage(generics.CreateAPIView, generics.RetrieveAPIView):
    serializer_class = PlayStageSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        player = Player.objects.filter(user=self.request.user).first()
        if player is None:
            return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)
        if player.game_play_stage is None or player.game_play_stage.is_completed:
            return Response({
                'current_phase': None,
                'is_playing': False
            })
        return Response({
            'current_phase': GamePlaySerializer(player.game_play_stage.current_game_play).data,
            'is_playing': True
        })

    def post(self, request, *args, **kwargs):
        serializer = PlayStageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        player = Player.objects.filter(user=self.request.user).first()
        if player is None:
            return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)

        if not player.validate_gem_equip():
            return Response({"error": "Gem equipment is not consistent"}, status=status.HTTP_400_BAD_REQUEST)

        if not player.validate_hero_slot():
            return Response({"error": "Hero is not consistent"}, status=status.HTTP_400_BAD_REQUEST)

        if player.game_play_stage is None or player.game_play_stage.is_completed or player.game_play_stage.current_game_play is None:
            # TODO Init HP State/Cooldown State

            skill_cool_down = {
                'slot1': 0,
                'slot2': 0,
                'slot3': 0,
                'slot4': 0,
                'slot5': 0,
            }
            hp = {
                'slot1': 100,
                'slot2': 100,
                'slot3': 100,
                'slot4': 100,
                'slot5': 100,
            }

            current_phase = serializer.validated_data['phase']

            if current_phase.phase_no > 1:
                return Response({"error": "Must start at phase 1"}, status=status.HTTP_400_BAD_REQUEST)
            is_boosted = False
            if serializer.validated_data['boost'] is True:
                if player.gold < current_phase.stage.boost_cost:
                    return Response({"error": "Not enough gold"}, status=status.HTTP_400_BAD_REQUEST)
                player.gold -= current_phase.stage.boost_cost
                is_boosted = True

            if current_phase.stage.require_stage is not None:
                if not GamePlayStage.objects.filter(stage=current_phase.stage.require_stage, player=player,
                                                    is_win=True).exists():
                    return Response({"error": "Must complete previous stage"}, status=status.HTTP_400_BAD_REQUEST)

            if player.get_current_stamina < current_phase.stage.stamina_cost:
                return Response({"error": "Not enough stamina"}, status=status.HTTP_400_BAD_REQUEST)

            # TODO Deduct stamina from player
            player.stamina_last_updated_value = player.get_current_stamina - current_phase.stage.stamina_cost
            player.stamina_last_updated = timezone.now()

            game_play_stage = GamePlayStage.objects.create(stage=current_phase.stage, player=player,
                                                           is_boosted=is_boosted)
            player.game_play_stage = game_play_stage
        else:
            game_play_stage = player.game_play_stage
            current_game_play = game_play_stage.current_game_play

            skill_cool_down = current_game_play.skill_cool_down
            hp = current_game_play.result_hp
            current_phase_no = current_game_play.phase.phase_no + 1
            current_phase = Phase.objects.filter(stage=current_game_play.phase.stage, phase_no=current_phase_no).first()

            # Reset player game state if no next phase
            if current_phase is None:
                game_play_stage.is_completed = True
                game_play_stage.save()
                return Response({"error": "Phase doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

            if current_phase != serializer.validated_data['phase']:
                return Response({"error": "Phase mismatch. Next phase id is " + str(current_phase.pk)},
                                status=status.HTTP_400_BAD_REQUEST)

        has_next_phase = Phase.objects.filter(stage=current_phase.stage, phase_no=current_phase.phase_no + 1).exists()

        # TODO Calculate game sequence

        is_win = True

        play_data = {
            'hero': HeroUserSlotSerializer(player.team_slot_data).data,
            # Is next phase avalable
            'game_sequence': [
                {
                    'from': 'e1',
                    'damages': [
                        {
                            'to': 'h2',
                            'damage': 240,
                            'left': 199,
                            "inflict_status": {
                                "name": "poison",
                                "turn": 2
                            }
                        },
                    ],
                    'type': 'normal'
                },
                {
                    'from': 'h1',
                    'damages': [
                        {
                            'to': 'e1',
                            'damage': 999,
                            'left': 1,
                            "inflict_status": None
                        }
                    ],
                    'type': 'normal'
                },
                {
                    'from': 'h2',
                    'damages': [
                        {
                            'to': 'e1',
                            'damage': 999,
                            'left': 0,
                            "inflict_status": None
                        }
                    ],
                    'type': 'skill'
                }
            ]
        }

        # TODO calculate result HP and Cooldown at the end of phase

        result_skill_cool_down = {
            'slot1': 2,
            'slot2': 3,
            'slot3': 1,
            'slot4': 0,
            'slot5': 0,
        }

        result_hp = {
            'slot1': 0,
            'slot2': 0,
            'slot3': 20,
            'slot4': 1,
            'slot5': 1,
        }

        game_play = GamePlay.objects.create(phase=current_phase, game_play_stage=game_play_stage,
                                            skill_cool_down=result_skill_cool_down, start_hp=hp, result_hp=result_hp,
                                            play_data=play_data, is_win=is_win)

        is_boosted = game_play_stage.is_boosted

        # TODO transfer reward to player if win
        player.gold += current_phase.reward["gold"]
        #player.coin_processing += current_phase.reward["coin"]
        player.coin_pending += current_phase.reward["coin"]

        game_play_stage.current_game_play = game_play

        if not is_win or not has_next_phase:
            game_play_stage.is_completed = True
            game_play_stage.is_win = is_win
            game_play_stage.current_game_play = None
            player.game_play_stage = None
        game_play_stage.save()
        player.save()
        return Response(GamePlaySerializer(game_play).data)
