
$(document).ready(function(){
  const $analysisDropdown = $('#id_analysis');
  const $vectorLayer = $('.vector_layer');
  const $supplyLayer = $('.supply_layer');
  const $showPercentage = $('.show_percentage');
  const $category = $('.category');

  $vectorLayer.hide();
  $supplyLayer.hide();
  $showPercentage.hide();

  $analysisDropdown.change(e => {
    let selectedAnalysis = e.target.value;
    $category.hide();

    if (selectedAnalysis === 'supply' || selectedAnalysis === 'ccp') {
      $vectorLayer.show();
      if (selectedAnalysis === 'supply') {
        $category.show();
      }
    } else {
      $vectorLayer.hide();
    }

    if (selectedAnalysis === 'ani') {
      $supplyLayer.show();
    } else {
      $supplyLayer.hide();
    }

    if (selectedAnalysis === 'ani' || selectedAnalysis === 'supply' || selectedAnalysis === 'ccp') {
      $showPercentage.show();
    } else {
      $showPercentage.hide();
    }
  })

  $analysisDropdown.change();
})