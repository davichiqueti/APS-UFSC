from views.tela_ranking import TelaRanking
from database.connection_factory import db_connection
from datetime import date, timedelta
import sqlalchemy


class ControladorRanking:
    def __init__(self, controlador_sistema):
        self.controlador_sistema = controlador_sistema
        self.tela_ranking = TelaRanking(self)

    def __pegarDataInicialPeriodo(self, periodo: int) -> date:
        """
        Retorna a data inicial para cada tipo de periodo.
        """
        hoje = date.today()
        match periodo:
            case 7:
                return hoje - timedelta(days=hoje.weekday())
            case 30:
                return hoje.replace(day=1)
            case 90:
                target_year = hoje.year
                target_month = hoje.month - 2
                if target_month < 1:
                    target_month += 12
                    target_year -= 1
                return hoje.replace(year=target_year, month=target_month)
            case 180:
                target_year = hoje.year
                target_month = hoje.month - 5
                if target_month < 1:
                    target_month += 12
                    target_year -= 1
                return hoje.replace(year=target_year, month=target_month)

    def gerarListagemRanking(self, tipo: str, periodo: int | None):
        match tipo:
            case "Número de Treinos":
                return self.gerarRankingPorContagem(periodo)
            case "Tempo em Atividade":
                return self.gerarRankingPorDuracao(periodo)
            case "Sequência de Treinos":
                return self.gerarRankingPorSequencia()

    def gerarRankingPorContagem(self, periodo: int):
        data_inicial = self.__pegarDataInicialPeriodo(periodo)
        query = sqlalchemy.text("""
            SELECT
                usuarios.nome,
                count(1) AS pontuacao
            FROM treinos
            INNER JOIN usuarios ON treinos.usuario = usuarios.id
            WHERE treinos."data" >= :data
            GROUP BY usuarios.nome
            ORDER BY
                pontuacao DESC,
                MAX("data") DESC,
                usuarios.nome
            LIMIT 15;
        """)
        results = db_connection.execute(
            statement=query,
            parameters={"data": data_inicial.isoformat()}
        )
        return results.fetchall()

    def gerarRankingPorDuracao(self, periodo: int):
        data_inicial = self.__pegarDataInicialPeriodo(periodo)
        query = sqlalchemy.text("""
            SELECT
                usuarios.nome,
                sum(duracao) AS pontuacao
            FROM treinos
            INNER JOIN usuarios ON treinos.usuario = usuarios.id
            WHERE treinos."data" >= '2025-05-26'
            GROUP BY usuarios.nome
            ORDER BY
                pontuacao DESC,
                MAX("data") DESC,
                usuarios.nome
            LIMIT 15;
        """)
        results = db_connection.execute(
            statement=query,
            parameters={"data": data_inicial.isoformat()}
        )
        return results.fetchall()

    def gerarRankingPorSequencia(self):
        query = sqlalchemy.text("""
            WITH dias_treinados AS (
                SELECT DISTINCT usuario, "data"::date
                FROM treinos
            ),
            treinos_numerados AS (
                SELECT
                    usuario,
                    "data",
                    ROW_NUMBER() OVER (PARTITION BY usuario
                ORDER BY "data") AS rn
                FROM dias_treinados
            ),
            agrupamentos AS (
                SELECT
                    usuario,
                    "data",
                    "data" - rn * INTERVAL '1 day' AS grupo
                FROM treinos_numerados
            ),
            sequencias AS (
                SELECT
                    usuario,
                    COUNT(*) AS dias_consecutivos,
                    MAX("data") AS data_final
                FROM agrupamentos
                GROUP BY usuario, grupo
            ),
            melhor_sequencia_por_usuario AS (
                SELECT
                    usuario,
                    MAX(dias_consecutivos) AS pontuacao,
                    MAX(data_final) AS data_mais_recente
                FROM sequencias
                GROUP BY usuario
            )
            SELECT
                u.nome,
                m.pontuacao
            FROM melhor_sequencia_por_usuario m
            JOIN usuarios u ON u.id = m.usuario
            ORDER BY
                m.pontuacao DESC,
                m.data_mais_recente DESC,
                u.nome
            LIMIT 15;
        """)
        results = db_connection.execute(statement=query)
        return results.fetchall()
