const micButton = document.getElementById("micButton");
const micText = document.getElementById("micText");
const originalText = document.getElementById("originalText");
const translatedText = document.getElementById("translatedText");

const sourceLanguage = document.getElementById("sourceLanguage");
const targetLanguage = document.getElementById("targetLanguage");

const speakButton = document.getElementById("speakButton");

const speechLanguages = {
    en: "en-US",
    hi: "hi-IN",
    kn: "kn-IN"
};


// ===============================
// MICROPHONE / SPEECH RECOGNITION
// ===============================

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

if (!SpeechRecognition) {

    micText.textContent =
        "Speech recognition is not supported ❌";

} else {

    const recognition =
        new SpeechRecognition();

    recognition.continuous = false;
    recognition.interimResults = false;


    micButton.addEventListener("click", () => {

        recognition.lang =
            speechLanguages[sourceLanguage.value] ||
            "en-US";

        micText.textContent =
            "Listening... 🎤";

        try {

            recognition.start();

        } catch (error) {

            console.log(
                "Recognition already started:",
                error
            );
        }
    });


    recognition.onresult = async (event) => {

        const text =
            event.results[0][0].transcript;

        originalText.textContent =
            text;

        micText.textContent =
            "Translating... ⏳";


        try {

            const response =
                await fetch(
                    "http://127.0.0.1:5000/translate",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            text: text,

                            source_language:
                                sourceLanguage.value,

                            target_language:
                                targetLanguage.value
                        })
                    }
                );


            const data =
                await response.json();


            console.log(
                "Backend response:",
                data
            );


            if (data.error) {

                throw new Error(
                    data.error
                );
            }


            translatedText.textContent =
                data.translation;


            micText.textContent =
                "Translation ready ✅";


        } catch (error) {

            console.error(
                "Translation error:",
                error
            );


            translatedText.textContent =
                "Translation failed.";


            micText.textContent =
                "Translation server error ❌";
        }
    };


    recognition.onerror = (event) => {

        console.error(
            "Speech error:",
            event.error
        );

        micText.textContent =
            "Microphone error ❌";
    };


    recognition.onend = () => {

        console.log(
            "Speech recognition ended."
        );
    };
}



// ===============================
// PLAY TRANSLATION
// ===============================

speakButton.addEventListener(
    "click",
    () => {

        const text =
            translatedText.textContent.trim();


        if (
            !text ||
            text ===
            "Your translation will appear here..."
        ) {
            return;
        }


        const speech =
            new SpeechSynthesisUtterance(text);


        speech.lang =
            speechLanguages[
                targetLanguage.value
            ] || "en-US";


        speech.rate = 0.9;
        speech.pitch = 1;


        window.speechSynthesis.cancel();


        window.speechSynthesis.speak(
            speech
        );
    }
);