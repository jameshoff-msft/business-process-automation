// import pdf from '../images/pdf.svg'
// import sentiment from '../images/sentimentDemoLogo.svg'
// import detectLanguage from '../images/detectLanguageDemoLogo.svg'
// import ner from '../images/nerDemoLogo.svg'
// import ocr from '../images/ocrLogo.svg'
// import summarize from '../images/summarizationDemoLogo.svg'
// import tts from '../images/textToSpeech.svg'
// import pii from '../images/piiDemoLogo.svg'
// import keyphrase from '../images/keyPhrasesDemoLogo.svg'
// import linkedEntities from '../images/linkedEntitiesDemoLogo.svg'
// import customNER from '../images/customEntityExtractionLogo.svg'
// import customClassification from '../images/customEntityExtractionLogo.svg'
// import customform from '../images/customform.svg'
// import generaldoc from '../images/customform.svg'
 import idcard from '../images/idcard.svg'
 import invoice from '../images/invoice.svg'
// import layoutLogo from '../images/layoutLogo.svg'
// import receipt from '../images/receiptcard.svg'
// import taxw2 from '../images/taxw2.svg'
// import businesscard from '../images/businesscard.svg'
// import storage from '../images/storage.svg'
// import wav from '../images/wav.svg'
import openai from '../images/openai.svg'
import { noCharge } from './Prices/price'
//import { getContentModeratorPricing, getCustomLanguagePricing, getDocumentTranslatorPricing, getFormRecCustomPricing, getFormRecPrebuiltPricing, getFormRecReadPricing, getHealthLanguagePricing, getLanguagePricing, getOcrPricing, getSpeechPricing, getTranslationPricing, noCharge } from './Prices/price'

export const inferenceCatalog = {
    "utterance": {
        "bpaServiceId": "abc123",
        "inputTypes": [
            "start","text"
        ],
        "outputTypes": [
            "text"
        ],
        "image": null,
        "label": "Utterance",
        "name": "utterance",
        "serviceSpecificConfig": {},
        "serviceSpecificConfigDefaults": {},
        getPrice : noCharge
    },
    "prompt": {
        "bpaServiceId": "abc123",
        "inputTypes": [
            "text"
        ],
        "outputTypes": [
            "text"
        ],
        "image": null,
        "label": "Prompt",
        "name": "prompts",
        "serviceSpecificConfig": {},
        "serviceSpecificConfigDefaults": {},
        getPrice : noCharge
    },
    "openai": {
        "bpaServiceId": "abc123",
        "inputTypes": [
            "text"
        ],
        "outputTypes": [
            "text"
        ],
        "image": openai,
        "label": "Open AI Completion/Chat",
        "name": "openai",
        "serviceSpecificConfig": {},
        "serviceSpecificConfigDefaults": {},
        getPrice : noCharge
    },
}