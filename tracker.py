import math

class Tracker:
    def __init__(self):
        # Emmagatzema les posicions centrals dels objectes detectats
        self.center_points = {}
        # Comptador d'identificadors únics (IDs)
        # Cada cop que es detecta un nou objecte, s'incrementa en un
        self.id_count = 0

    def update(self, objects_rect):
        # Llista per emmagatzemar les caixes delimitadores d'objectes i els seus IDs
        objects_bbs_ids = []

        # Calcula el punt central de cada objecte detectat
        for rect in objects_rect:
            x, y, w, h = rect
            # Calcula el centre de la caixa delimitadora
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Variable per verificar si l'objecte ja ha estat detectat
            same_object_detected = False

            # Compara el punt central actual amb punts centrals emmagatzemats
            for id, pt in self.center_points.items():
                # Calcula la distància entre el punt central actual i el registrat
                dist = math.hypot(cx - pt[0], cy - pt[1])

                # Si la distància és menor a 35, es considera el mateix objecte
                if dist < 35:
                    # Actualitza la posició del punt central de l'objecte
                    self.center_points[id] = (cx, cy)
                    # Afegeix l'objecte a la llista amb el seu ID
                    objects_bbs_ids.append([x, y, w, h, id])
                    # Marca l'objecte com a detectat
                    same_object_detected = True
                    break

            # Si l'objecte no s'havia detectat abans, se li assigna un nou ID
            if same_object_detected is False:
                # Afegeix el nou objecte amb un ID únic al diccionari
                self.center_points[self.id_count] = (cx, cy)
                # Afegeix l'objecte a la llista amb el seu ID
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                # Incrementa el comptador d'ID per al següent objecte nou
                self.id_count += 1

        # Crea un nou diccionari per actualitzar les posicions dels punts centrals
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            # Obté l'ID de l'objecte
            _, _, _, _, object_id = obj_bb_id
            # Obté el punt central associat a aquest ID
            center = self.center_points[object_id]
            # Afegeix l'ID i el punt central al nou diccionari
            new_center_points[object_id] = center

        # Actualitza el diccionari de punts centrals eliminant IDs no utilitzats
        self.center_points = new_center_points.copy()
        return objects_bbs_ids
