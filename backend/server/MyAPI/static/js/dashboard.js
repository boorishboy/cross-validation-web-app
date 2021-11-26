$(document).ready(function() {

  function getFileName(string) {
    var urlSplit = string.split('/');
    return urlSplit[urlSplit.length - 1];
  }

  function truncateContent(string) {
    if (string.includes(", ")) {
      var list = string.split(",")
      if (list.length > 10) {
        var slicedArray = list.slice(0, 10);
        return slicedArray;
      } else {
        return list;
      }
    } else {
      var list = string.split(" ")
      if (list.length > 10) {
        var slicedArray = list.slice(0, 10);
        return slicedArray;
      } else {
        return list;
      }
    }
  }

  // function getLabels(array) {
  //   var xlables = [];
  //   for (let i = 1; i - 1 < array.length; i++) {
  //     xlables.push(i.toString())
  //   }
  //   return xlables;
  // }
  //
  // function getErrorArray(array, data) {
  //   var errorArray = [];
  //   for (let i = 0; i < array.length; i++) {
  //     errorArray.push(data.results.rkf_stddev)
  //   }
  //   return errorArray;
  // }
  //
  // function getMeanArray(array, data) {
  //   var meanArray = [];
  //   for (let i = 0; i < array.length; i++) {
  //     meanArray.push(data.results.rkf_mean)
  //   }
  //   return meanArray;
  // }


  $('select').change(function() {
    value = $(this).val();
    $.ajax({
      url: "/api/combined/" + value + "/",
      type: "GET",
      dataType: "json",
      success: (data) => {

        var dataRKF = data.results.rkf_scores.replace(/[\[\]']+/g, '').split(", ");
        dataRKF = dataRKF.map(numStr => parseFloat(numStr));
        var dataCV = data.results.cv_scores.replace(/[\[\]']+/g, '').split(", ");
        dataCV = dataCV.map(numStr => parseFloat(numStr));
        // if (RKFChart) {
        //   RKFChart.destroy();
        // } else {
        //   var ctx = document.getElementById('data-val-rkf').getContext('2d');
        //   var RKFChart = new Chart(ctx, {
        //     type: 'bar',
        //     data: {
        //       labels: getLabelNumbers(dataRKF),
        //       datasets: [{
        //         label: 'RKF Score',
        //         data: dataRKF,
        //         backgroundColor: [
        //           'rgba(255, 99, 132, 0.2)',
        //           'rgba(54, 162, 235, 0.2)',
        //           'rgba(255, 206, 86, 0.2)',
        //           'rgba(75, 192, 192, 0.2)',
        //           'rgba(153, 102, 255, 0.2)',
        //           'rgba(255, 159, 64, 0.2)'
        //         ],
        //         borderColor: [
        //           'rgba(255, 99, 132, 1)',
        //           'rgba(54, 162, 235, 1)',
        //           'rgba(255, 206, 86, 1)',
        //           'rgba(75, 192, 192, 1)',
        //           'rgba(153, 102, 255, 1)',
        //           'rgba(255, 159, 64, 1)'
        //         ],
        //         borderWidth: 1
        //       }]
        //     },
        //     options: {
        //       locale: 'pl-PL',
        //       tooltips: {
        //         mode: 'index',
        //         intersect: false
        //       },
        //       scales: {
        //         y: {
        //           beginAtZero: true
        //         }
        //       }
        //     }
        //   });
        // }




        var paramTableBody = $("#parameters-table tbody")
        var resultOlsTableBody = $("#results-ols-table tbody")
        var resultNnlsTableBody = $("#results-nnls-table tbody")
        var dataValTableBody = $("#data-val-table tbody")
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
                  
                  var valueDataVal = () => (typeof(item)=="string") ? item.replace(/[\[\]']+/g, '') : item;
                  var valueDataVal = item;
                  // } else if (i == "resultid" || valuesToPass.includes(i)) {
                  //   var keyDataVal = i;
                  //   var valueDataVal = item;


                  dataValTableBody.append(
                    "<tr>" +
                    "<th>" + keyDataVal + "</th>" +
                    "<td>" + valueDataVal + "</td>" +
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
                    var valueOls = item;
                  }
                  resultOlsTableBody.append(
                    "<tr>" +
                    "<th>" + keyOls + "</th>" +
                    "<td>" + valueOls + "</td>" +
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
                    var valueNnls = item;
                  }
                  resultNnlsTableBody.append(
                    "<tr>" +
                    "<th>" + keyNnls + "</th>" +
                    "<td>" + valueNnls + "</td>" +
                    "</tr>"
                  );
                }
              })

            }
          } else {

          }


          // var trace1 = {
          //   x: getLabels(dataRKF),
          //   y: dataRKF,
          //   name: 'RKF Scores',
          //   error_y: {
          //     type: 'data',
          //     array: getErrorArray(dataRKF, data),
          //     visible: true
          //   },
          //   type: 'bar'
          // };
          // var trace2 = {
          //   x: getLabels(dataRKF),
          //   y: getMeanArray(dataRKF, data),
          //   name: 'Mean',
          //   type: 'line'
          // };
          // var data1 = [trace1, trace2];
          // var layout = {
          //   title: 'RepeatedKFold Scores',
          //   titlefont: {
          //     family: 'Roboto',
          //     size: 18,
          //   },
          //   xaxis: {
          //     'type': 'category',
          //     title: 'Number of Fold',
          //     titlefont: {
          //       family: 'Roboto',
          //       size: 18,
          //       color: 'lightgrey'
          //     }
          //   },
          //   autosize: true,
          //   // shapes: [{
          //   //     type: 'line',
          //   //     x0: 1,
          //   //     y0: 0,
          //   //     x1: 1,
          //   //     y1: 2,
          //   //     line: {
          //   //       color: 'rgb(55, 128, 191)',
          //   //       width: 3
          //   //     }
          //   //   }
          //   // ]
          // };
          // var config = {
          //   locale: 'pl',
          //   responsive: true,
          // };
          //
          //
          //
          // Plotly.newPlot('data-val-rkf-plot', data1, layout, config);
        });
        plotRKF(dataRKF, data);
        plotCV(dataCV, data);
      },
      error: (error) => {
        console.log(error);
      }
    });
  });

});
