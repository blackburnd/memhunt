import sys
import gc
import logging
from tempfile import NamedTemporaryFile
from typing import Optional, Union
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader, Template
except ImportError:
    # Fallback if Jinja2 is not available
    Environment = None
    FileSystemLoader = None
    Template = None

import objgraph as objgraph_lib
from pympler import muppy, summary

# Initialize pympler for memory tracking
memory_tracker = muppy
logger = logging.getLogger(__name__)


class BaseView:
    """Base view class for memory debugging tools"""
    
    def __init__(self, context=None, request=None):
        self.context = context
        self.request = request
        self._setup_templates()
    
    def _setup_templates(self):
        """Set up Jinja2 template environment"""
        if Environment is None:
            logger.warning("Jinja2 not available, templates will be disabled")
            self.jinja_env = None
            return
            
        # Get the directory containing the templates
        current_dir = Path(__file__).parent
        template_dir = current_dir / "templates"
        
        # Fallback to zpt directory if templates doesn't exist
        if not template_dir.exists():
            template_dir = current_dir / "zpt"
            
        if template_dir.exists():
            self.jinja_env = Environment(
                loader=FileSystemLoader(str(template_dir)),
                autoescape=True
            )
        else:
            logger.warning(f"Template directory not found: {template_dir}")
            self.jinja_env = None
    
    def render_template(self, template_name: str, **context) -> str:
        """Render a Jinja2 template with given context"""
        if self.jinja_env is None:
            return f"Template system not available. Template: {template_name}"
            
        try:
            template = self.jinja_env.get_template(template_name)
            context['view'] = self
            context['context'] = self.context
            context['request'] = self.request
            return template.render(**context)
        except Exception as e:
            logger.error(f"Error rendering template {template_name}: {e}")
            return f"Error rendering template: {e}"
    
    def render_simple_template(self, template_string: str, **context) -> str:
        """Render a simple template string"""
        if Template is None:
            return template_string
            
        try:
            template = Template(template_string)
            context['view'] = self
            return template.render(**context)
        except Exception as e:
            logger.error(f"Error rendering template string: {e}")
            return template_string


class Start(BaseView):
    """Start page view for memory debugging tools"""
    
    def __call__(self) -> str:
        title = "Memory and Reference Counting Tools"
        return self.render_template("start.html", title=title)


class RefCount(BaseView):
    """Reference counting view"""
    
    def __call__(self) -> str:
        self.update()
        return self.render_template("ref_count.html",
                                    pairs=self.pairs,
                                    total_ref_count=self.total_ref_count,
                                    garbage_containing=self.garbage_containing,
                                    garbage_watching=self.garbage_watching)
        
    def update(self) -> None:
        try:
            res = {}
            # collect all classes
            self.garbage_containing = len(gc.garbage)
            self.garbage_watching = len(gc.get_objects())
            self.total_ref_count = 0

            for mod in sys.modules.values():
                if mod is None:
                    continue
                for attr in dir(mod):
                    try:
                        obj = getattr(mod, attr)
                        if isinstance(obj, type):
                            res[obj] = sys.getrefcount(obj)
                    except (AttributeError, TypeError) as e:
                        logger.debug(f"Error accessing {attr}: {e}")
                        continue

            # sort by refcount
            pairs = [(repr(x[0]), x[1]) for x in res.items()]
            pairs.sort(key=lambda x: x[1], reverse=True)

            self.pairs = []
            for pair in pairs:
                self.total_ref_count += pair[1]
                self.pairs.append({'refcount': pair[1],
                                   'name': pair[0]})

            self.pairs = sorted(self.pairs, key=lambda x: x['refcount'])
            self.pairs.reverse()
        except Exception as e:
            logger.error(f"Error in update method: {e}")
            self.pairs = []
            self.total_ref_count = 0
            self.garbage_containing = 0
            self.garbage_watching = 0

    @property
    def target(self) -> Optional[type]:
        try:
            if getattr(self, '_target', None):
                return getattr(self, '_target')

            target = self.request.form.get('name', '')
            if not target:
                return None

            target = target.strip('<').strip('>')
            target = '_'.join(target.split(' ')[:-1])

            coll = {}
            for m in sys.modules.values():
                if m is None:
                    continue
                for sym in dir(m):
                    try:
                        o = getattr(m, sym)
                        if isinstance(o, type):
                            repr_str = repr(o).strip('<').strip('>')
                            name_parts = repr_str.split(' ')[:-1]
                            name = '_'.join(name_parts)
                            coll[name] = o
                    except (AttributeError, TypeError) as e:
                        logger.debug(f"Error processing symbol {sym}: {e}")
                        continue

            self._target = coll.get(target, None)
            return self._target
        except Exception as e:
            logger.error(f"Error in target property: {e}")
            return None

    def view_backref(self) -> Union[str, bytes]:
        if self.target is None:
            return "Please select an item to introspect"
        return self.back_ref_file

    def view_ref(self) -> Union[str, bytes]:
        if self.target is None:
            return "Please select an item to introspect"
        return self.ref_file

    @property
    def ref_file(self) -> bytes:
        try:
            self.request.response.setHeader('content-type', 'image/png')
            with NamedTemporaryFile('wb', suffix='.png', delete=False) as f:
                objgraph_lib.show_refs([self.target], max_depth=6, filename=f.name)
                with open(f.name, 'rb') as img_file:
                    return img_file.read()
        except Exception as e:
            logger.error(f"Error generating reference graph: {e}")
            return b"Error generating reference graph"

    @property
    def back_ref_file(self) -> bytes:
        try:
            self.request.response.setHeader('content-type', 'image/png')
            with NamedTemporaryFile('wb', suffix='.png', delete=False) as f:
                objgraph_lib.show_backrefs([self.target], max_depth=6, filename=f.name)
                with open(f.name, 'rb') as img_file:
                    return img_file.read()
        except Exception as e:
            logger.error(f"Error generating back-reference graph: {e}")
            return b"Error generating back-reference graph"

    def context_refs(self) -> bytes:
        self._target = self.context
        return self.ref_file

    def context_backrefs(self) -> bytes:
        self._target = self.context
        return self.back_ref_file


class DebugView(BaseView):
    """Debug view for memory analysis"""
    __allow_access_to_unprotected_subobjects__ = 1

    def most_common(self) -> str:
        pairs = objgraph_lib.most_common_types()
        self.pairs = []
        for pair in pairs:
            self.pairs.append({'refcount': pair[1],
                               'name': pair[0]})

        return self.render_template("ref_common_count.html", pairs=self.pairs)

    def display_mem(self) -> str:
        try:
            import malloc_stats
            return malloc_stats.malloc_stats()
        except ImportError:
            return "malloc_stats module not available"
        except Exception as e:
            logger.error(f"Error getting malloc stats: {e}")
            return f"Error getting malloc stats: {e}"

    def reset_heap(self) -> str:
        # Reset memory tracking baseline for testing
        # Note: pympler doesn't have exact equivalent to guppy's setrelheap
        return "Memory tracking reset (pympler doesn't support heap reset)"

    def memory(self) -> str:
        try:
            all_objects = muppy.get_objects()
            mem_summary = summary.summarize(all_objects)
            return '\n'.join(summary.format_(mem_summary))
        except Exception as e:
            logger.error(f"Error getting memory summary: {e}")
            return f"Error getting memory summary: {e}"

    # Print memory consumption summary
    def relative_memory(self) -> str:
        try:
            all_objects = muppy.get_objects()
            mem_summary = summary.summarize(all_objects)
            return '\n'.join(summary.format_(mem_summary))
        except Exception as e:
            logger.error(f"Error getting relative memory: {e}")
            return f"Error getting relative memory: {e}"

    def by_referrers(self) -> str:
        all_objects = muppy.get_objects()
        mem_summary = summary.summarize(all_objects)
        # Sort by size (closest equivalent to byrcs)
        sorted_summary = sorted(mem_summary, key=lambda x: x[2], reverse=True)
        return '\n'.join(summary.format_(sorted_summary))

    def get_biggest_offender(self) -> str:
        try:
            all_objects = muppy.get_objects()
            mem_summary = summary.summarize(all_objects)
            if mem_summary:
                biggest = max(mem_summary, key=lambda x: x[2])
                res = "BIGGEST OFFENDER:\\n"
                res += f"Type: {biggest[0]}\\n"
                res += f"Count: {biggest[1]}\\n"
                res += f"Total Size: {biggest[2]} bytes\\n"
                return res
            return "No memory data available"
        except Exception as e:
            logger.error(f"Error getting biggest offender: {e}")
            return f"Error getting biggest offender: {e}"

    # Print memory consumption with detailed analysis
    def traverse_relative_memory(self) -> str:
        try:
            all_objects = muppy.get_objects()
            mem_summary = summary.summarize(all_objects)
            # Get top 40 items (equivalent to get_rp(40))
            if len(mem_summary) >= 40:
                top_40 = mem_summary[:40]
            else:
                top_40 = mem_summary
            return '\n'.join(summary.format_(top_40))
        except Exception as e:
            logger.error(f"Error getting traverse relative memory: {e}")
            return f"Error getting traverse relative memory: {e}"

    def breakpoint(self) -> str:
        # Removed pdb.set_trace() for security reasons
        # Use proper logging or debugging tools instead
        return "Breakpoint functionality disabled for security"
