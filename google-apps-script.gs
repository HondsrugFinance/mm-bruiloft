// Mike & Martine — Google Apps Script Backend
// Deploy as: New → Web app → Execute as: Me → Anyone (anonymous)

function doPost(e) {
  try {
    const payload = JSON.parse(e.postData.contents);
    const base64 = payload.file;
    const gast = payload.gast || "Onbekend";
    const apparaat = payload.apparaat || "unknown";
    const bestandsnaam = payload.naam || "foto.jpg";

    if (!base64) {
      return ContentService.createTextOutput(JSON.stringify({
        error: "Geen bestand"
      })).setMimeType(ContentService.MimeType.JSON);
    }

    // Decode base64
    const bytes = Utilities.base64Decode(base64);
    const blob = Utilities.newBlob(bytes, "image/jpeg", bestandsnaam);

    // Get or create main folder
    const mainFolder = getOrCreateFolder("MM_Bruiloft_Fotos");

    // Get or create device subfolder
    const deviceFolder = getOrCreateSubfolder(mainFolder, apparaat);

    // Save file
    const file = deviceFolder.createFile(blob);
    file.setName(bestandsnaam);

    // Log to sheet
    const sheet = getOrCreateSheet();
    sheet.appendRow([
      new Date(),
      gast,
      apparaat,
      bestandsnaam,
      file.getId()
    ]);

    return ContentService.createTextOutput(JSON.stringify({
      success: true,
      id: file.getId(),
      pad: apparaat + "/" + bestandsnaam
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({
      error: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  if (e.parameter.action === "health") {
    return ContentService.createTextOutput(JSON.stringify({
      status: "ok"
    })).setMimeType(ContentService.MimeType.JSON);
  }

  const sheet = getOrCreateSheet();
  const data = sheet.getDataRange().getValues();
  const devices = new Set();
  for (let i = 1; i < data.length; i++) {
    devices.add(data[i][2]);
  }

  return ContentService.createTextOutput(JSON.stringify({
    total_fotos: Math.max(0, data.length - 1),
    unique_devices: devices.size
  })).setMimeType(ContentService.MimeType.JSON);
}

function getOrCreateFolder(folderName) {
  const folders = DriveApp.getFoldersByName(folderName);
  if (folders.hasNext()) {
    return folders.next();
  }
  return DriveApp.createFolder(folderName);
}

function getOrCreateSubfolder(parentFolder, subfolderName) {
  const subfolders = parentFolder.getFoldersByName(subfolderName);
  if (subfolders.hasNext()) {
    return subfolders.next();
  }
  return parentFolder.createFolder(subfolderName);
}

function getOrCreateSheet() {
  const props = PropertiesService.getUserProperties();
  const sheetId = props.getProperty("MM_SHEET_ID");

  let spreadsheet;
  if (sheetId) {
    try {
      spreadsheet = SpreadsheetApp.openById(sheetId);
    } catch (e) {
      spreadsheet = null;
    }
  }

  if (!spreadsheet) {
    spreadsheet = SpreadsheetApp.create("MM Bruiloft Fotos");
    props.setProperty("MM_SHEET_ID", spreadsheet.getId());
  }

  let sheet = spreadsheet.getSheetByName("Fotos");
  if (!sheet) {
    sheet = spreadsheet.insertSheet("Fotos", 0);
    sheet.appendRow(["Datum", "Gast", "Apparaat", "Bestand", "Drive ID"]);
  }

  return sheet;
}
