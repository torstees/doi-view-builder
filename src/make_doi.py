#!/usr/bin/env python
import json

from pathlib import Path

from argparse import ArgumentParser, FileType

import pdb

html_template = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <style>
      body {
        font-family: Arial, Helvetica, sans-serif;
      }
      ul {
        list-style-type: none;
      }

      .data-container {
        width: 90%;
        margin: 20px 0 0 20px;
      }

      .title-div {
        font-size: 20px;
        font-weight: 600;
        padding: 0 0 10px 0;
        color: rgb(34, 38, 77);
      }
      .headers-row {
        display: flex;
        flex-direction: column;
      }

      .toggle-row {
        display: flex;
      }

      .toggle-header {
        cursor: pointer;
        padding: 10px;
        background-color: #f0f0f0;
        border: 1px solid #ccc;
        font-size: 20px;
        font-weight: 600;
        color: rgb(34, 38, 77);
        padding: 10px 20px;
      }

      .toggle-header.active-header {
        color: rgb(100, 152, 228);
      }

      .toggle-content {
        display: none; /* Initially hide all toggle-content */
        padding: 10px;
        background-color: #f9f9f9;
        border-top: 1px solid #ccc;
      }

      .active {
        display: block; /* Show the active toggle-content */
      }
    </style>

    <title></title>
  </head>
  <body>
    <div id="metadata-container"></div>
    <script>
      const jsonData = $JSON_DATA_HERE;
      document.title = jsonData.titles[0].title;

      // Create content for description, creators, and contributors
      const descriptionContent = `
  <ul>${jsonData.descriptions
    .map((desc) => {
      return `<li>${desc.description}</li>`; // Ensure we return the description
    })
    .join(", ")}</ul>
`;

      const creatorsContent = `
  <ul>
    ${jsonData.creators
      .map((creator) => `<li>${creator.name != null ? creator.name : ""}</li>`)
      .join("")}
  </ul>
`;

      const contributorsContent = `
  <ul>
    ${jsonData.contributors
      .map(
        (contributor) =>
          `<li>${contributor.name != null ? contributor.name : ""}</li>`
      )
      .join("")}
  </ul>
`;

      const relatedIdentifiersContent = `<ul>${
        jsonData.relatedIdentifiers.length > 0
          ? jsonData.relatedIdentifiers
              .map(
                (identifier) => `<div>
      <p>${
        identifier.schemeUri != null
          ? `<b>Scheme URI:</b> ${identifier.schemeUri}`
          : ""
      }</p>
      <p>${
        identifier.schemeType != null
          ? `<b>Scheme Type:</b> ${identifier.schemeType}`
          : ""
      }</p>
      <p>${
        identifier.relationType != null
          ? `<b>Relation Type:</b> ${identifier.relationType}`
          : ""
      }</p>
      <p>${
        identifier.relatedIdentifier != null
          ? `<b>Related Identifier:</b> ${identifier.relatedIdentifier}`
          : ""
      }</p>
      <p>${
        identifier.resourceTypeGeneral != null
          ? `<b>Resource Type General:</b> ${identifier.resourceTypeGeneral}`
          : ""
      }</p>
      <p>${
        identifier.relatedIdentifierType != null
          ? `<b>Related Identifier Type:</b> ${identifier.relatedIdentifierType}`
          : ""
      }</p>
      <p>${
        identifier.relatedMetadataScheme != null
          ? `<b>Related Metadata Scheme:</b> ${identifier.relatedMetadataScheme}`
          : ""
      }</p>
    </div>`
              )
              .join("<br>")
          : ""
      } </ul>`;

      // Create rows for description, creators, and contributors
      let pageDisplay = `
      <div class="data-container">
    ${
      jsonData.titles.length > 0
        ? jsonData.titles
            .map((titleObj) => `<div class="title-div">${titleObj.title}</div>`)
            .join("")
        : ""
    }
        
  <div><p><b>DOI:</b> ${jsonData.doi != null ? jsonData.doi : ""}</p>
  <p> ${
    jsonData.types.resourceType != null
      ? ` <b>Resource Type: </b>${jsonData.types.resourceType}`
      : ""
  }</p>
  <p>
  ${
    jsonData.publisher && jsonData.publicationYear
      ? `Published by ${jsonData.publisher.name} in ${jsonData.publicationYear}`
      : jsonData.publisher
      ? jsonData.publisher.name
      : ""
      ? `Published by ${jsonData.publisher.name}`
      : jsonData.publicationYear
      ? `Published ${jsonData.publicationYear}`
      : ""
  }
</p>

  </div>
  
<div class="headers-row">
    <div class="toggle-row">
        <div class="toggle-header">Description</div>
        <div class="toggle-header">Creators</div>
        <div class="toggle-header">Contributors</div>
        <div class="toggle-header">Related Identifiers</div>  
    </div>
    <div class="toggle-content">${descriptionContent}</div>
    <div class="toggle-content">${creatorsContent}</div>
    <div class="toggle-content">${contributorsContent}</div>
    <div class="toggle-content">${relatedIdentifiersContent}</div>
</div>
</div>

`;

      document.getElementById("metadata-container").innerHTML = pageDisplay;

      // Click event listeners to toggle the visibility of each section
      const headers = document.querySelectorAll(".toggle-header");

      // Add click event listeners to each header
      headers.forEach((header, index) => {
        header.addEventListener("click", () => {
          // Hide all toggle-content sections
          const allContents = document.querySelectorAll(".toggle-content");
          allContents.forEach((content) => content.classList.remove("active"));

          // Show the content corresponding to the clicked header
          const content = allContents[index];
          content.classList.add("active");

          // Remove the active class from all headers and add it to the clicked one
          headers.forEach((header) => header.classList.remove("active-header"));
          header.classList.add("active-header");
        });
      });

      // Make sure the first header's content is visible by default
      const firstContent = document.querySelectorAll(".toggle-content")[0];
      const firstHeader = document.querySelectorAll(".toggle-header")[0];
      if (firstContent) {
        firstContent.classList.add("active");
        firstHeader.classList.add("active-header");
      }
    </script>
  </body>
</html>
"""


def main():
    parser = ArgumentParser(description="Creates HTML file for viewing DOI")
    parser.add_argument(
        "files", nargs="+", type=FileType("rt"), help="JSON DOI files for HTML viewing"
    )
    args = parser.parse_args()

    # Iterate over each of the JSON files provided by user
    for doi_json in args.files:
        # Open file using json library and convert that into a string.
        # I recommend using indent=2 when converting to a string for readability.
        # See https://docs.python.org/3/library/json.html
        json_data = json.load(doi_json)
        json_string = json.dumps(json_data, indent=2)

        # Using the html template above, html_template, use basic python text
        # replacement to replace the variable $JSON_DATA_HERE with the string version
        # of the actual DOI JSON data
        html_content = html_template.replace("$JSON_DATA_HERE", json_string)

        # Using the Path library, we can create an HTML filename based on the
        # original filename.
        html_filename = Path(Path(doi_json.name).stem + ".html")

        with html_filename.open("wt") as outfile:
            outfile.write(html_content)


if __name__ == "__main__":
    main()
