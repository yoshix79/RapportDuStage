from flask import Flask, render_template, session, redirect, url_for, request, jsonify
import pandas as pd
from db import get_db_connection


def is_valid_detection_data(data):
    required = ['name', 'date', 'time']
    return data and all(key in data for key in required)


def load_detections_from_csv(filepath=None):
    # Chargement depuis MySQL (plus de CSV)
    detections = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM logs ORDER BY date_pointage DESC, heure_pointage DESC LIMIT 100")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        for row in rows:
            detections.append({
                'name': row['nom_prenom'],
                'date': row['date_pointage'].strftime('%Y-%m-%d') if hasattr(row['date_pointage'], 'strftime') else str(row['date_pointage']),
                'time': str(row['heure_pointage']),
                'status': row['statut'],
                'image_path': row['image']
            })
    except Exception as e:
        print(f"Erreur lors du chargement des détections depuis la base : {e}")
    return detections


def get_detection_statistics(filepath=None):
    stats = {'total': 0, 'pourcentage_reconnus': 0, 'nb_alertes': 0}
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) AS total FROM logs")
        stats['total'] = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) AS count FROM logs WHERE LOWER(nom_prenom) != 'inconnu'")
        nb_reconnus = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) AS count FROM logs WHERE LOWER(nom_prenom) = 'inconnu'")
        nb_inconnus = cursor.fetchone()['count']

        total_valid = nb_reconnus + nb_inconnus
        if total_valid > 0:
            stats['pourcentage_reconnus'] = round((nb_reconnus * 100) / total_valid, 2)

        cursor.execute("""
            SELECT COUNT(*) AS alertes FROM (
                SELECT nom_prenom, COUNT(*) AS nb
                FROM logs
                GROUP BY nom_prenom
                HAVING nb > 6
            ) AS subquery
        """)
        stats['nb_alertes'] = cursor.fetchone()['alertes']

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erreur lors du calcul des statistiques : {e}")
    return stats


def detection_exists(name, date, time, status, filepath=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT 1 FROM logs
            WHERE nom_prenom = %s AND date_pointage = %s AND heure_pointage = %s AND statut = %s
            LIMIT 1
        """
        cursor.execute(query, (name, date, time, status))
        exists = cursor.fetchone() is not None
        cursor.close()
        conn.close()
        return exists
    except Exception as e:
        print(f"Erreur lors de la vérification de détection : {e}")
        return False


def log_detection(name, date, time, statut, image_path, filepath=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO logs (nom_prenom, date_pointage, heure_pointage, statut, image)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, date, time, statut, image_path))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erreur lors de l'enregistrement de la détection : {e}")
