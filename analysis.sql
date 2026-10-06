CREATE OR REPLACE VIEW match_analysis AS
WITH match_stats AS (
    SELECT
        match_id,
        TO_TIMESTAMP((raw_data ->> 'game_creation')::BIGINT / 1000.0) AS game_datetime,
        (raw_data ->> 'queue_id')::INTEGER AS queue_id,
        CASE
            WHEN raw_data ->> 'championName' = 'Chogath' THEN 'Cho''Gath'
            WHEN raw_data ->> 'championName' = 'TahmKench' THEN 'Tahm Kench'
            WHEN raw_data ->> 'championName' = 'MissFortune' THEN 'Miss Fortune'
            ELSE raw_data ->> 'championName'
            END AS champion,
        CASE
            WHEN raw_data ->> 'individualPosition' = 'UTILITY' THEN 'SUPPORT'
            ELSE raw_data ->> 'individualPosition'
        END AS role,
        (raw_data ->> 'win')::BOOLEAN AS win,
        (raw_data ->> 'kills')::INTEGER AS kills,
        (raw_data ->> 'deaths')::INTEGER AS deaths,
        (raw_data ->> 'assists')::INTEGER AS assists,
        (raw_data ->> 'totalMinionsKilled')::INTEGER AS minions_killed,
        (raw_data ->> 'neutralMinionsKilled')::INTEGER AS neutral_minions_killed,
        (raw_data ->> 'goldEarned')::INTEGER AS gold_earned,
        (raw_data ->> 'totalDamageDealtToChampions')::INTEGER AS total_damage_to_champions,
        (raw_data ->> 'visionScore')::INTEGER AS vision_score,
        (raw_data ->> 'game_duration')::INTEGER AS game_duration,
        (raw_data -> 'challenges' ->> 'damagePerMinute')::NUMERIC AS damage_per_minute,
        (raw_data -> 'challenges' ->> 'goldPerMinute')::NUMERIC AS gold_per_minute,
        (raw_data -> 'challenges' ->> 'killParticipation')::NUMERIC AS kill_participation,
        (raw_data -> 'challenges' ->> 'laneMinionsFirst10Minutes')::NUMERIC AS cs_at_10,
        (raw_data -> 'challenges' ->> 'soloKills')::INTEGER AS solo_kills,
        (raw_data -> 'challenges' ->> 'turretPlatesTaken')::INTEGER AS turret_plates_taken,
        (raw_data -> 'challenges' ->> 'visionScorePerMinute')::NUMERIC AS vision_score_per_minute,
        (raw_data -> 'challenges' ->> 'kda')::NUMERIC AS kda
    FROM raw_matches
)

SELECT
    *,
    ROUND(game_duration / 60.0, 2) AS game_duration_minutes,
    minions_killed + neutral_minions_killed AS total_cs,
    ROUND(
        (minions_killed + neutral_minions_killed) / (game_duration / 60.0),
        2
    ) AS cs_per_minute
FROM match_stats;