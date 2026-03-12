import { initializeApp } from "firebase/app"
import { getFirestore } from "firebase/firestore"

const firebaseConfig = {
  apiKey: "AIzaSyB_PUhh0zuZkM7bDdqtohoSoDJVEFAM-uo",
  authDomain: "bot-marcelofloricultura.firebaseapp.com",
  projectId: "bot-marcelofloricultura",
  storageBucket: "bot-marcelofloricultura.firebasestorage.app",
  messagingSenderId: "640050114744",
  appId: "1:640050114744:web:29c7eef48906946f75044d",
  measurementId: "G-2NQQZBM9DR"
};

const app = initializeApp(firebaseConfig)

export const db = getFirestore(app)