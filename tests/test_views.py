"""
Modern test suite for memhunt
"""
import pytest
from unittest.mock import Mock, patch

# Import the classes we want to test
from memhunt.browser.views import Start, RefCount, DebugView


class TestStart:
    """Test the Start view"""
    
    def test_start_view_instantiation(self):
        """Test that Start view can be instantiated"""
        context = Mock()
        request = Mock()
        view = Start(context, request)
        assert view is not None
        assert view.context == context
        assert view.request == request
    
    def test_start_view_call(self):
        """Test that Start view __call__ method works"""
        context = Mock()
        request = Mock()
        view = Start(context, request)
        
        # Mock the render_template method
        view.render_template = Mock(return_value="<html>test</html>")
        
        result = view()
        assert result == "<html>test</html>"
        view.render_template.assert_called_once()


class TestRefCount:
    """Test the RefCount view"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.context = Mock()
        self.request = Mock()
        self.request.form = {}
        self.request.response = Mock()
        self.view = RefCount(self.context, self.request)
    
    def test_refcount_view_instantiation(self):
        """Test that RefCount view can be instantiated"""
        assert self.view is not None
        assert self.view.context == self.context
        assert self.view.request == self.request
    
    def test_update_method(self):
        """Test the update method"""
        # Mock the render_template method to avoid template loading issues
        self.view.render_template = Mock()
        
        self.view.update()
        
        # Check that basic attributes are set
        assert hasattr(self.view, 'pairs')
        assert hasattr(self.view, 'total_ref_count')
        assert hasattr(self.view, 'garbage_containing')
        assert hasattr(self.view, 'garbage_watching')
        
        assert isinstance(self.view.pairs, list)
        assert isinstance(self.view.total_ref_count, int)
        assert isinstance(self.view.garbage_containing, int)
        assert isinstance(self.view.garbage_watching, int)
    
    def test_target_property_no_name(self):
        """Test target property when no name is provided"""
        self.request.form = {}
        result = self.view.target
        assert result is None
    
    def test_target_property_with_name(self):
        """Test target property with a name"""
        self.request.form = {'name': '<class \'str\'>'}
        # The target might be None if the class isn't found, which is expected
        result = self.view.target
        # Just check it doesn't crash
        assert result is None or isinstance(result, type)
    
    def test_view_backref_no_target(self):
        """Test view_backref when no target is selected"""
        self.view._target = None
        result = self.view.view_backref()
        assert result == "Please select an item to introspect"
    
    def test_view_ref_no_target(self):
        """Test view_ref when no target is selected"""
        self.view._target = None
        result = self.view.view_ref()
        assert result == "Please select an item to introspect"
    
    @patch('memhunt.browser.views.objgraph_lib.show_refs')
    def test_ref_file_with_target(self, mock_show_refs):
        """Test ref_file property with a valid target"""
        self.view._target = str  # Use str as a test target
        self.request.response.setHeader = Mock()
        
        # Mock the file operations
        with patch('tempfile.NamedTemporaryFile') as mock_temp:
            mock_file = Mock()
            mock_file.name = '/tmp/test.png'
            mock_temp.return_value.__enter__.return_value = mock_file
            
            with patch('builtins.open', create=True) as mock_open:
                mock_file_content = b'fake_image_data'
                mock_read = mock_open.return_value.__enter__.return_value.read
                mock_read.return_value = mock_file_content
                
                result = self.view.ref_file
                
                assert result == b'fake_image_data'
                expected_call = ('content-type', 'image/png')
                response_mock = self.request.response.setHeader
                response_mock.assert_called_with(*expected_call)


class TestDebugView:
    """Test the DebugView"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.context = Mock()
        self.request = Mock()
        self.view = DebugView(self.context, self.request)
    
    def test_debug_view_instantiation(self):
        """Test that DebugView can be instantiated"""
        assert self.view is not None
        assert self.view.context == self.context
        assert self.view.request == self.request
    
    @patch('memhunt.browser.views.objgraph_lib.most_common_types')
    def test_most_common(self, mock_most_common):
        """Test most_common method"""
        mock_most_common.return_value = [('dict', 100), ('list', 50)]
        
        # Mock the render_template method
        self.view.render_template = Mock(return_value="<html>common types</html>")
        
        result = self.view.most_common()
        
        assert result == "<html>common types</html>"
        assert len(self.view.pairs) == 2
        assert self.view.pairs[0]['name'] == 'dict'
        assert self.view.pairs[0]['refcount'] == 100
    
    def test_memory_method(self):
        """Test memory method"""
        result = self.view.memory()
        # Should return a string (formatted memory summary)
        assert isinstance(result, str)
        # Should not crash
        assert len(result) > 0
    
    def test_relative_memory_method(self):
        """Test relative_memory method"""
        result = self.view.relative_memory()
        # Should return a string (formatted memory summary)
        assert isinstance(result, str)
        # Should not crash
        assert len(result) > 0
    
    def test_reset_heap_method(self):
        """Test reset_heap method"""
        result = self.view.reset_heap()
        # Should return a string indicating reset is not supported
        assert isinstance(result, str)
        assert "reset" in result.lower()
    
    def test_by_referrers_method(self):
        """Test by_referrers method"""
        result = self.view.by_referrers()
        # Should return a string (formatted memory summary)
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_get_biggest_offender_method(self):
        """Test get_biggest_offender method"""
        result = self.view.get_biggest_offender()
        # Should return a string with biggest offender info
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_traverse_relative_memory_method(self):
        """Test traverse_relative_memory method"""
        result = self.view.traverse_relative_memory()
        # Should return a string (formatted memory summary)
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_breakpoint_method(self):
        """Test breakpoint method (should be disabled)"""
        result = self.view.breakpoint()
        # Should return security message
        assert isinstance(result, str)
        assert "security" in result.lower()
    
    def test_display_mem_method(self):
        """Test display_mem method"""
        result = self.view.display_mem()
        # Should return a string (either malloc stats or error message)
        assert isinstance(result, str)


class TestIntegration:
    """Integration tests"""
    
    def test_garbage_collection_interaction(self):
        """Test that the views work with garbage collection"""
        context = Mock()
        request = Mock()
        request.form = {}
        request.response = Mock()
        
        view = RefCount(context, request)
        view.template = Mock()
        
        # This should not crash even with real garbage collection
        view.update()
        
        assert isinstance(view.garbage_containing, int)
        assert isinstance(view.garbage_watching, int)
        assert view.garbage_containing >= 0
        assert view.garbage_watching >= 0
    
    def test_memory_tracking_basic(self):
        """Test basic memory tracking functionality"""
        context = Mock()
        request = Mock()
        
        debug_view = DebugView(context, request)
        
        # These should all return strings and not crash
        memory_result = debug_view.memory()
        relative_result = debug_view.relative_memory()
        biggest_result = debug_view.get_biggest_offender()
        
        assert isinstance(memory_result, str)
        assert isinstance(relative_result, str)
        assert isinstance(biggest_result, str)
        
        assert len(memory_result) > 0
        assert len(relative_result) > 0
        assert len(biggest_result) > 0


if __name__ == '__main__':
    pytest.main([__file__])
