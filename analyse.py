import cv2
import numpy as np
import matplotlib.pyplot as plt




# # camera matrix en distorion coefficients van IPHONE 12 bron apple/developer
# camera_matrix = np.array([[5.24255310e+02, 0.00000000e+00, 3.20000000e+02],
#                           [0.00000000e+00, 5.24255310e+02, 1.07819000e+03],
#                           [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]], dtype=np.float32)

# dist_coeffs = np.array([-1.66795522e-01, 2.40551416e-01, -1.25831251e-03, -5.86340381e-04, 1.60331414e-01], dtype=np.float32)
fpsopname = 214.06
meetlat_lengte_in_werkelijkheid = 5 # in m


afstand = []
tijd = []
punten = []


# Lees het videobestand in
cap = cv2.VideoCapture('video\IMG_0562.MOV')

# Maak een tracker aan
tracker = cv2.TrackerCSRT_create()

# Haal de frames per seconde van de video op
fps = cap.get(cv2.CAP_PROP_FPS)  

delay_frames = int(4 * fps)  # Aantal frames voor 4 seconden

# Lees en toon frames tot de gewenste tijd is bereikt
for _ in range(delay_frames):
    ret, frame = cap.read()
frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE) 

# cameralens correctie
# frame = cv2.undistort(frame, camera_matrix, dist_coeffs)

cv2.imshow('Tracking', frame)
cv2.waitKey(1)

# Selecteer het object dat je wilt volgen
bbox = cv2.selectROI('Tracking', frame, False)

# Maak een muis callback functie
def select_points(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        punten.append((x, y))
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow('image', frame)


# Maak een venster en stel de muis callback functie in
cv2.namedWindow('image')
cv2.setMouseCallback('image', select_points)

# Toon het beeld tot twee punten zijn geselecteerd
while len(punten) < 2:
    cv2.imshow('image', frame)
    cv2.waitKey(1000)  # Wacht voor 1 seconde
    print(punten)

# Bereken de lengte van de meetlat in pixels
meetlat_lengte_in_pixels = ((punten[1][0] - punten[0][0]) ** 2 + (punten[1][1] - punten[0][1]) ** 2) ** 0.5


# Controleer of de bbox geldige waarden bevat
if bbox[2] > 0 and bbox[3] > 0:
    # Initialiseer de tracker met het geselecteerde object
    tracker.init(frame, bbox)
else:
    print("Geen geldige ROI geselecteerd!")
    cap.release()
    cv2.destroyAllWindows()
    exit()
    
    
# Initialiseer de tracker met het geselecteerde object
tracker.init(frame, bbox)

# Bepaal de schaal van de video
# Dit is afhankelijk van uw specifieke video en kan variëren
scale = meetlat_lengte_in_werkelijkheid / meetlat_lengte_in_pixels

# Initialiseer de vorige positie van het object
curr_pos = (bbox[0], bbox[1])

while True:
    # Lees het volgende frame van de video
    ret, frame = cap.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)    

    # Als er geen frame meer is, stop dan de loop
    if not ret:
        break
    
    # cameralens correctie
    # frame = cv2.undistort(frame, camera_matrix, dist_coeffs)


    # Update de tracker met het nieuwe frame
    ret, bbox = tracker.update(frame)

    # Als de tracker het object niet meer kan volgen, stop dan de loop
    if not ret:
        break

    # Bereken de huidige positie van het object
    prev_pos = (bbox[0], bbox[1])

    # Bereken de afgelegde afstand in pixels
    dist_pixels = ((curr_pos[0] - prev_pos[0]) ** 2 + (curr_pos[1] - prev_pos[1]) ** 2) ** 0.5

    # Voeg de afstand toe aan de lijst
    afstand.append(dist_pixels * scale)  # Afstand in werkelijke eenheden

    # haal de afspeel fps op
    afspeelfps = cap.get(cv2.CAP_PROP_FPS)
    # bereken slowmotion factor
    slowmotionfactor = fpsopname / afspeelfps
    # bereken de tijd
    curr_time = (cap.get(cv2.CAP_PROP_POS_MSEC) / 1000) / slowmotionfactor

    # Voeg de tijd toe aan de lijst
    tijd.append(curr_time)

    # Update de vorige positie en tijd
    prev_pos = curr_pos
    prev_time = curr_time
        
    

    # Teken een rechthoek rondom het object
    cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])), (0, 255, 0), 2)

    # Toon het frame
    cv2.imshow('Tracking', frame)

    # Wacht op een toetsdruk
    if cv2.waitKey(1) == ord('q'):
        break

# Sluit de video
cap.release()

# Sluit de vensters
cv2.destroyAllWindows()

# Bereken de snelheid en versnelling van het object
snelheid = np.gradient(afstand, tijd)
versnelling = np.gradient(snelheid, tijd)

gemiddelde_snelheid = np.mean(snelheid)
gemiddelde_versnelling = np.mean(versnelling)


# Fit een polynomiale functie van de tweede graad (parabool) aan de snelheid
snelheid_coef = np.polyfit(tijd, snelheid, 1)
snelheid_poly = np.poly1d(snelheid_coef)

# Fit een polynomiale functie van de tweede graad (parabool) aan de versnelling
versnelling_coef = np.polyfit(tijd, versnelling, 1)
versnelling_poly = np.poly1d(versnelling_coef)

print("Functievergelijking voor snelheid: \n", snelheid_poly)
print("Functievergelijking voor versnelling: \n", versnelling_poly)

# Plot afstand, snelheid en versnelling in één grafiek
plt.figure(figsize=(10, 6))

plt.subplot(3, 1, 1)
plt.plot(tijd, afstand)
plt.xlabel('Tijd (s)')
plt.ylabel('Afstand (m)')
plt.title('Afstand van het object in de tijd')

plt.subplot(3, 1, 2)
plt.plot(tijd, snelheid)
plt.axhline(gemiddelde_snelheid, color='r', linestyle='--')  # Voeg de gemiddelde snelheid toe
plt.xlabel('Tijd (s)')
plt.ylabel('Snelheid (m/s)')
plt.title('Snelheid van het object in de tijd')

plt.subplot(3, 1, 3)
plt.plot(tijd, versnelling)
plt.axhline(gemiddelde_versnelling, color='r', linestyle='--')  
plt.xlabel('Tijd (s)')
plt.ylabel('Versnelling (m/s²)')
plt.title('Versnelling van het object in de tijd')

plt.tight_layout()
plt.show()