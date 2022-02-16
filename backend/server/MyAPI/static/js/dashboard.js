$(document).ready(function() {

  function getFileName(string) {
    var urlSplit = string.split('/');
    return urlSplit[urlSplit.length - 1];
  }

  function truncateContent(string) {
    if (string.includes(", ")) {
      let list = string.replace(/[\[\]']+/g, '').split(",");
      if (list.length > 10) {
        let slicedArray = list.slice(0, 10);
        slicedArray.push(" ...");
        return slicedArray;
      } else {
        return list;
      }
    } else {
      string.replace(/[\[\]']+/g, '');
      let list = string.replace(/[\[\]']+/g, '').split(" ");
      if (list.length > 10) {
        let slicedArray = list.slice(0, 10);
        slicedArray.push(" ...");
        return slicedArray;
      } else {
        return list;
      }
    }
  }

  function syntaxHighlight(json) {
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function(match) {
      var cls = 'number';
      if (/^"/.test(match)) {
        if (/:$/.test(match)) {
          cls = 'key';
        } else {
          cls = 'string';
        }
      } else if (/true|false/.test(match)) {
        cls = 'boolean';
      } else if (/null/.test(match)) {
        cls = 'null';
      }
      return '<span class="' + cls + '">' + match + '</span>';
    });
  }

  function download(content, fileName, contentType) {
    const a = document.createElement("a");
    const file = new Blob([content], {
      type: contentType
    });
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
  }

  function StringArrayToFloat(responseData) {
    return responseData.replace(/[\[\]']+/g, '').split(", ").map(numStr => parseFloat(numStr));
  }




  $('select').change(function() {
    value = $(this).val();
    $.ajax({
      url: "/api/combined/" + value + "/",
      type: "GET",
      dataType: "json",
      success: (data) => {
        var dataRKF = StringArrayToFloat(data.results.rkf_scores);
        var dataCV = StringArrayToFloat(data.results.cv_scores)
        var y_data = StringArrayToFloat(data.results.y)
        var percentage_error_vect_ols = StringArrayToFloat(data.results.percentage_error_vect_ols)
        var coefs_ols = StringArrayToFloat(data.results.coefs_ols)
        var percentage_error_vect_nnls = StringArrayToFloat(data.results.percentage_error_vect_nnls)
        var coefs_nnls = StringArrayToFloat(data.results.coefs_nnls)


        var paramTableBody = $("#parameters-table tbody")
        var resultOlsTableBody = $("#results-ols-table tbody")
        var resultNnlsTableBody = $("#results-nnls-table tbody")
        var dataValTableBody = $("#data-val-table tbody")
        var jsonDiv = $('#json-data')
        var jsonString = JSON.stringify(data, null, 4);
        jsonDiv.empty();
        jsonDiv.append(syntaxHighlight(jsonString));
        $("#json-download").click(function () {download(JSON.stringify(data, null, 4), data.runid.toString() + "_" + data.targetColumn + "_" + data.upload_timestamp + ".json", "text/json"); });
        paramTableBody.empty();
        resultOlsTableBody.empty();
        resultNnlsTableBody.empty();
        dataValTableBody.empty();
        $.each(data, function(i, item) {
          if (i != 'results') {
            var key = i;
            if (item == null) {
              var value = "-";
            } else if (i == "inputFile") {
              var value = getFileName(item);
            } else if (i == "upload_timestamp") {
              var value = moment(item).format('DD-MM-YYYY, HH:mm:ss:SSS');
            } else {
              var value = item;
            }

            paramTableBody.append(
              "<tr>" +
              "<th>" + key + "</th>" +
              "<td>" + value + "</td>" +
              "</tr>"
            );

          } else if (i == 'results') {
            var valuesToPass = ["upload_timestamp", "file_hash", "runid"]
            var dataValScores = ["rkf_mean", "rkf_scores", "rkf_stddev", "cv_mean", "cv_scores", "cv_stddev"]
            if (data.results != null) {
              $.each(data.results, function(i, item) {
                if (dataValScores.includes(i)) {
                  var keyDataVal = i;

                  var valueDataVal = (typeof(item) == 'string') ? item.replace(/[\[\]']+/g, '') : item;


                  dataValTableBody.append(
                    "<tr>" +
                    "<th>" + keyDataVal + "</th>" +
                    "<td data-toggle='tooltip' data-placement='top' title='Full data in Raw Data tab'>" + valueDataVal + "</td>" +
                    "</tr>"
                  );

                } else if (valuesToPass.includes(i)) {
                  return true;
                } else if (i.includes("ols")) {
                  var keyOls = i;
                  if (item == null) {
                    var valueOls = "-";
                  } else if (i == 'results_timestamp') {
                    var valueOls = moment(item).format('DD-MM-YYYY, HH:mm:ss:SSS');
                  } else if (item == "[]") {
                    var valueOls = "-";
                  } else if (typeof(item) == 'string') {
                    if (item.includes('[')) {
                      var valueOls = truncateContent(item);
                    }
                  } else {
                    var valueOls = (typeof(item) == 'string') ? item.replace(/[\[\]']+/g, '') : item;
                  }
                  resultOlsTableBody.append(
                    "<tr>" +
                    "<th>" + keyOls + "</th>" +
                    "<td data-toggle='tooltip' data-placement='top' title='Full data in Raw Data tab'>" + valueOls + "</td>" +
                    "</tr>"
                  );
                } else if (i.includes("nnls")) {
                  var keyNnls = i;
                  if (item == null) {
                    var valueNnls = "-";
                  } else if (i == 'results_timestamp') {
                    var valueNnls = moment(item).format('DD-MM-YYYY, HH:mm:ss:SSS');
                  } else if (item == "[]") {
                    var valueNnls = "-";
                  } else if (typeof(item) == 'string') {
                    if (item.includes('[')) {
                      var valueNnls = truncateContent(item);
                    }
                  } else {
                    var valueNnls = (typeof(item) == 'string') ? item.replace(/[\[\]']+/g, '') : item;
                  }
                  resultNnlsTableBody.append(
                    "<tr>" +
                    "<th>" + keyNnls + "</th>" +
                    "<td data-toggle='tooltip' data-placement='top' title='Full data in Raw Data tab'>" + valueNnls + "</td>" +
                    "</tr>"
                  );
                }
              })

            }
          } else {

          }
        });
        plotRKF(dataRKF, data);
        plotCV(dataCV, data);
        plotOLS_first(y_data, percentage_error_vect_ols, data);
        plotOLSCoefs(coefs_ols, data);
        plotNNLS_eror(y_data, percentage_error_vect_nnls, data);
        plotNNLSCoefs(coefs_nnls, data);
        $("td").tooltip({
          container: 'body'
        });
      },
      error: (error) => {
        console.log(error);
      }
    });
  });

});
