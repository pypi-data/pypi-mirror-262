"""Test plugin schemas"""

from synodic_utilities.utility import TypeName

from cppython_core.plugin_schema.generator import SyncConsumer
from cppython_core.plugin_schema.provider import SyncProducer
from cppython_core.schema import SyncData


class TestSchema:
    """Test validation"""

    class GeneratorSyncDataSuccess(SyncData):
        """Dummy generator data"""

        success: bool

    class GeneratorSyncDataFail(SyncData):
        """Dummy generator data"""

        failure: bool

    class Consumer(SyncConsumer):
        """Dummy consumer"""

        @staticmethod
        def sync_types() -> list[type[SyncData]]:
            """Fulfils protocol

            Returns:
                Fulfils protocol
            """

            return [TestSchema.GeneratorSyncDataSuccess, TestSchema.GeneratorSyncDataFail]

        def sync(self, sync_data: SyncData) -> None:
            """Fulfils protocol

            Args:
                sync_data: Fulfils protocol
            """

            if isinstance(sync_data, TestSchema.GeneratorSyncDataSuccess):
                assert sync_data.success
            else:
                assert False

    class Producer(SyncProducer):
        """Dummy producer"""

        @staticmethod
        def supported_sync_type(sync_type: type[SyncData]) -> bool:
            """Fulfils protocol

            Args:
                sync_type: Fulfils protocol

            Returns:
                Fulfils protocol
            """
            return sync_type == TestSchema.GeneratorSyncDataSuccess

        def sync_data(self, consumer: SyncConsumer) -> SyncData | None:
            """Fulfils protocol

            Args:
                consumer: Fulfils protocol

            Returns:
                Fulfils protocol
            """
            for sync_type in consumer.sync_types():
                if sync_type == TestSchema.GeneratorSyncDataSuccess:
                    return TestSchema.GeneratorSyncDataSuccess(provider_name=TypeName("Dummy"), success=True)

            return None

    def test_sync_broadcast(self) -> None:
        """Verifies broadcast support"""

        consumer = self.Consumer()
        producer = self.Producer()

        types = consumer.sync_types()

        assert producer.supported_sync_type(types[0])
        assert not producer.supported_sync_type(types[1])

    def test_sync_production(self) -> None:
        """Verifies the variant behavior of SyncData"""

        producer = self.Producer()
        consumer = self.Consumer()
        assert producer.sync_data(consumer)

    def test_sync_consumption(self) -> None:
        """Verifies the variant behavior of SyncData"""

        consumer = self.Consumer()

        data = self.GeneratorSyncDataSuccess(provider_name=TypeName("Dummy"), success=True)
        consumer.sync(data)

    def test_sync_flow(self) -> None:
        """Verifies the variant behavior of SyncData"""

        consumer = self.Consumer()
        producer = self.Producer()

        types = consumer.sync_types()

        for test in types:
            if producer.supported_sync_type(test):
                if data := producer.sync_data(consumer):
                    consumer.sync(data)
