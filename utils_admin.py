from db import get_db_connection
from collections import Counter


def lire_utilisateurs_sql():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM utilisateurs")
        utilisateurs = cursor.fetchall()
        cursor.close()
        conn.close()
        return utilisateurs
    except Exception as e:
        print(f"Erreur lire_utilisateurs_sql: {e}")
        return []


def compter_utilisateurs_sql():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # On ne compte pas l’admin
        cursor.execute("SELECT COUNT(*) AS count FROM utilisateurs WHERE LOWER(name) != 'admin'")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result['count'] if result else 0
    except Exception as e:
        print(f"Erreur compter_utilisateurs_sql: {e}")
        return 0

def calculer_total_salaires_utilisateurs_sql():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT SUM(salary) AS total FROM utilisateurs")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return float(result['total']) if result and result['total'] else 0.0
    except Exception as e:
        print(f"Erreur calculer_total_salaires_utilisateurs_sql: {e}")
        return 0.0

def analyser_logs_sql():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) AS total_detections FROM logs")
        total_detections = cursor.fetchone()['total_detections']

        cursor.execute("SELECT COUNT(*) AS nb_reconnus FROM logs WHERE LOWER(Nom_Prenom) != 'inconnu'")
        nb_reconnus = cursor.fetchone()['nb_reconnus']

        percent_reconnus = round((nb_reconnus * 100) / total_detections, 2) if total_detections > 0 else 0

        # Compter les occurrences par personne (hors inconnu)
        cursor.execute("""
            SELECT LOWER(Nom_Prenom) AS nom, COUNT(*) AS count
            FROM logs
            WHERE LOWER(Nom_Prenom) != 'inconnu'
            GROUP BY LOWER(Nom_Prenom)
        """)
        rows = cursor.fetchall()
        counter = Counter()
        for row in rows:
            counter[row['nom']] = row['count']

        # Nb alertes : nom ayant >= 6 entrées
        nb_alertes = sum(1 for count in counter.values() if count >= 6)

        cursor.close()
        conn.close()

        return total_detections, nb_reconnus, percent_reconnus, nb_alertes, counter

    except Exception as e:
        print(f"Erreur analyser_logs_sql: {e}")
        return 0, 0, 0, 0, Counter()
