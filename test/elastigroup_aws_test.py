

class spotinst_sdk2:
	class models:
		class elastigroup:
			class aws:
				def Elastigroup():
					return MagicMock()
				def Compute():
					return MagicMock()
				def InstanceTypes():
					return MagicMock()
				def EbsVolume():
					return MagicMock()
				def CreditSpecification():
					return MagicMock()
				def ThirdPartyIntegrations():
					return MagicMock()
				def Route53Configuration():
					return MagicMock()
				def Scheduling():
					return MagicMock()
				def 

	class clients:
		class elastigroup:


	@pytest.fixture(autouse=True)
	def spotinst_sdk2(monkeypatch):
	    spotinst_sdk2 = MagicMock()
	    sys.modules['spotinst_sdk2'] = spotinst_sdk2

	    # monkeypatch.setattr(sys.modules, 'spotinst_sdk2', MagicMock())

	    return spotinst_sdk2


	@pytest.fixture(autouse=True)
	def spotinst(spotinst_sdk2):
	    import ansible.modules.cloud.spotinst.spotinst_aws_elastigroup as spotinst

	    return spotinst

