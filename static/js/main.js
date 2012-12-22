$(document).ready(function(){
    var transport = new Thrift.Transport("/thrift");
    var protocol  = new Thrift.Protocol(transport);
    var client    = new NewServiceClient(protocol);

    /*try {
      result = client.calculate(1, work);
      $('#result').val(result);
      $('#result').css('color', 'black');
    } catch(ouch){
      $('#result').val(ouch.why);
      $('#result').css('color', 'red');
    }*/
    $('#output').text(client.strcat('test', 'test'));
});
